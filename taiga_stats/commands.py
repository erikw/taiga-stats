import configparser
import datetime as dt
import os
import re
import sys
import time

import matplotlib  # noqa

matplotlib.use("TkAgg")  # noqa
import matplotlib.dates as mplotdates  # noqa
import matplotlib.pyplot as plt  # noqa
import numpy  # noqa
import taiga  # noqa
from matplotlib.dates import MONDAY, DateFormatter, WeekdayLocator  # noqa

import taiga_stats.constants as c  # noqa
from taiga_stats.helpers import get_dot_footer  # noqa
from taiga_stats.helpers import get_dot_header  # noqa
from taiga_stats.helpers import get_status_and_names_sorted  # noqa
from taiga_stats.helpers import get_statuses_sorted_by_order  # noqa
from taiga_stats.helpers import get_tag_str  # noqa
from taiga_stats.helpers import (assert_args, get_stories_with_tag,  # noqa
                                 get_us_status_name_from_id, read_daily_cfd)

CFD_OUT_PNG_FMT = "cfd_{:s}.png"
NO_ANNOTATION = "NONE"
DEPS_DOT_FILE_FMT = "dependencies_{:s}"


@assert_args("url", "auth_token")
def cmd_list_projects(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])

    print(
        "All projects which you have access to\n(note that this can take very very long if you use https://api.taiga.io/, as there are many projects):\n"
    )
    print("id\tname")
    print("--\t----")
    for proj in api.projects.list():
        print("{:-3d}\t{:s}".format(proj.id, proj.name))

    return 0


@assert_args("url", "auth_token", "project_id")
def cmd_list_us_statuses(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])

    print('Statuses for project "{:s}"'.format(project.name))
    print("order\tid\tname")
    print("--\t----")
    statuses = get_statuses_sorted_by_order(project)
    for status in statuses:
        print("{:d}\t{:-4d}\t{:s}".format(status.order, status.id, status.name))

    return 0


@assert_args("url", "auth_token", "project_id", "tag")
def cmd_print_us_in_dep_format(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])
    tag = args["tag"]
    status_ids = None

    status_ids, _ = get_status_and_names_sorted(project)
    selected_sids = None
    if "status_ids" in args and args["status_ids"]:
        selected_sids = [int(sid) for sid in args["status_ids"].split(",")]
        selected_sids.reverse()
    else:
        selected_sids = status_ids

    for sid in selected_sids:
        try:
            _ = status_ids.index(sid)
        except ValueError:
            print(
                "Selected US status ID {:d} not found for project {:s}!".format(
                    sid, project.name
                )
            )
            return 1

    uss = get_stories_with_tag(project, tag)

    selected_uss = []
    for us in uss:
        if us.status in selected_sids:
            selected_uss.append(us)

    for us in selected_uss:
        if us.is_closed:
            color = "green"
        else:
            color = "black"
        subject = re.sub('"', "", us.subject)
        print(
            '  "{:d}" [label="#{:d} {:s}", color="{:s}"];'.format(
                us.ref, us.ref, subject, color
            )
        )

    return 0


@assert_args(
    "url",
    "auth_token",
    "project_id",
    "tag",
    "output_path",
    "print_tags",
    "print_points",
)
def cmd_us_in_dep_format_dot(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])
    tag = args["tag"]
    output_path = args["output_path"]
    status_ids = None
    print_tags = args["print_tags"]
    print_points = args["print_points"]

    status_ids, _ = get_status_and_names_sorted(project)
    selected_sids = None
    if "status_ids" in args and args["status_ids"]:
        selected_sids = [int(sid) for sid in args["status_ids"].split(",")]
        selected_sids.reverse()
    else:
        selected_sids = status_ids

    for sid in selected_sids:
        try:
            _ = status_ids.index(sid)
        except ValueError:
            print(
                "Selected US status ID {:d} not found for project {:s}!".format(
                    sid, project.name
                )
            )
            return 1

    uss = get_stories_with_tag(project, tag)

    selected_uss = []
    for us in uss:
        if us.status in selected_sids:
            selected_uss.append(us)

    titles = []
    edges = []
    header = get_dot_header(
        get_tag_str(tag), "{:s} US Dependency Graph".format(get_tag_str(tag))
    )

    depson_attr_id = None
    proj_attrs = project.list_user_story_attributes()
    for attr in proj_attrs:
        if attr.name == c.CUST_ATTRIB_DEPENDSON_NAME:
            depson_attr_id = attr.id
    if not depson_attr_id:
        print(
            "No custom User Story attribute named '{:s}' found!. Go to Settings>Attributes>Custom Fields and create one.".format(
                c.CUST_ATTRIB_DEPENDSON_NAME
            ),
            file=sys.stderr,
        )
        return 1

    for us in selected_uss:
        if us.is_closed:
            color = "green"
        else:
            color = "black"
        subject = re.sub('"', "", us.subject)

        points = ""
        if print_points and us.total_points:
            points += "\n{:s} points".format(str(us.total_points))
            points = points.replace("\n", "\\n")  # Don't interpret \n.

        tags = ""
        if print_tags and us.tags:
            tags += "\n["
            for ustag in us.tags:
                tags += "{:s}, ".format(ustag)
            tags = tags[:-2]  # Remove last ", "
            tags += "]"
            tags = tags.replace("\n", "\\n")  # Don't interpret \n.

        attrs = us.get_attributes()
        if str(depson_attr_id) in attrs["attributes_values"]:
            deps = attrs["attributes_values"][str(depson_attr_id)].split(",")
            for dep in deps:
                dep = dep.strip(" \t\n\r").lstrip("#")
                if dep:
                    edges.append('  "{:s}" -> "{:d}"'.format(dep, us.ref))

        titles.append(
            '  "{:d}" [label="#{:d} {:s}{:s}{:s}", color="{:s}"];'.format(
                us.ref, us.ref, subject, tags, points, color
            )
        )

    footer = get_dot_footer()
    titles.sort()
    edges.sort()

    file_name_base = DEPS_DOT_FILE_FMT.format(get_tag_str(tag))
    file_name = file_name_base + ".dot"
    file_path = "{:s}/{:s}".format(output_path, file_name)
    try:
        with open(file_path, "w") as fh:
            fh.write(header)
            fh.write("\n  // Edges\n")
            for edge in edges:
                fh.write("{:s}\n".format(edge))
            fh.write("\n  // Titles\n")
            for title in titles:
                fh.write("{:s}\n".format(title))
            fh.write(footer)
            print("Dependency graph written to: {:s}\n".format(file_path))
            print("Generate a png with e.g.")
            print(
                "$ dot -T png -o {:s}/{:s}.png {:s}".format(
                    output_path, file_name_base, file_path
                )
            )
            print(
                "$ unflatten -l1 -c5 {:s}/{:s} | dot -T png -o {:s}/{:s}.png".format(
                    output_path, file_name, output_path, file_name_base
                )
            )
    except IOError as err:
        print(
            "Could not write file {:s}: {:s}".format(file_path, str(err)),
            file=sys.stderr,
        )
        return 1

    return 0


@assert_args("url", "auth_token", "project_id", "tag")
def cmd_points_sum(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])
    tag = args["tag"]
    status_ids = None

    status_ids, _ = get_status_and_names_sorted(project)
    selected_sids = None
    if "status_ids" in args and args["status_ids"]:
        selected_sids = [int(sid) for sid in args["status_ids"].split(",")]
        selected_sids.reverse()
    else:
        selected_sids = status_ids

    for sid in selected_sids:
        try:
            _ = status_ids.index(sid)
        except ValueError:
            print(
                "Selected US status ID {:d} not found for project {:s}!".format(
                    sid, project.name
                )
            )
            return 1

    uss = get_stories_with_tag(project, tag)

    selected_uss = []
    for us in uss:
        if us.status in selected_sids:
            selected_uss.append(us)

    points = {}  # statusID -> pointsum
    for us in selected_uss:
        if us.status not in points:
            points[us.status] = 0
        if us.total_points:
            points[us.status] += float(us.total_points)

    for status_id, points_sum in points.items():
        status_name = get_us_status_name_from_id(project, status_id)
        print("{:20s}\t{:.1f}".format(status_name, points_sum))


@assert_args("url", "auth_token", "project_id", "tag")
def cmd_print_burnup_data(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])
    tag = args["tag"]
    status_ids = None

    status_ids, status_names = get_status_and_names_sorted(project)
    selected_sids = None
    if "status_ids" in args and args["status_ids"]:
        selected_sids = [int(sid) for sid in args["status_ids"].split(",")]
        selected_sids.reverse()
    else:
        selected_sids = status_ids

    selected_snames = []
    for sid in selected_sids:
        try:
            idx = status_ids.index(sid)
        except ValueError:
            print(
                "Selected US status ID {:d} not found for project {:s}!".format(
                    sid, project.name
                )
            )
            return 1
        selected_snames.append(status_names[idx])

    uss = get_stories_with_tag(project, tag)

    selected_uss = []
    for us in uss:
        if us.status in selected_sids:
            selected_uss.append(us)

    nbr_done = 0
    nbr_todo = 0
    nbr_pts_done = 0
    nbr_pts_todo = 0
    total_pts = 0
    for us in selected_uss:
        pts = 0
        if us.total_points:
            pts = float(us.total_points)
            total_pts += pts

        if us.is_closed:
            nbr_done += 1
            nbr_pts_done += pts
        else:
            nbr_todo += 1
            nbr_pts_todo += pts

    snames_str = ", ".join(reversed(selected_snames))
    tag_str = tag if tag != c.TAG_MATCH_ALL else "*"
    print("Statuses: {:s}".format(snames_str))
    print("Tag: {:s}".format(tag_str))
    print("##### User Stories #####")
    print("Total: {:d}".format(len(selected_uss)))
    print("Done: {:d}".format(nbr_done))
    print("TODO: {:d}".format(nbr_todo))
    print("##### Points #####")
    print("Total: {:.1f}".format(total_pts))
    print("Done: {:.1f}".format(nbr_pts_done))
    print("TODO: {:.1f}".format(nbr_pts_todo))

    return 0


@assert_args("url", "auth_token", "project_id", "tag", "output_path")
def cmd_store_daily_stats(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])
    tag = args["tag"]
    output_path = args["output_path"]

    status_ids, _ = get_status_and_names_sorted(project)
    uss = get_stories_with_tag(project, tag)
    us_by_status = {status_id: [] for status_id in status_ids}
    for us in uss:
        us_by_status[us.status].append(us)

    data_file = c.CFD_DATA_FILE_FMT.format(get_tag_str(tag))
    data_path = "{:s}/{:s}".format(output_path, data_file)
    if not os.path.isfile(data_path):
        with open(data_path, "w") as fdata:
            fdata.write("#date")
            fdata.write("\tannotation")
            fdata.write("\tannotation_layer")
            for status_id in status_ids:
                fdata.write(
                    "\t{:s}".format(get_us_status_name_from_id(project, status_id))
                )
            fdata.write("\n")

    with open(data_path, "a") as fdata:
        fdata.write("{:s}".format(dt.datetime.utcnow().strftime("%Y-%m-%d")))
        fdata.write("\t{:s}".format(NO_ANNOTATION))
        fdata.write("\t{:d}".format(0))
        for status_id in status_ids:
            no_uss = len(us_by_status[status_id])
            fdata.write("\t{:d}".format(no_uss))
        fdata.write("\n")

    tag_str = " for {:s}".format(tag) if tag != c.TAG_MATCH_ALL else ""
    print("Daily stats{:s} stored at: {:s}".format(tag_str, output_path))

    return 0


@assert_args("url", "auth_token", "project_id", "tag", "output_path", "annotations_off")
def cmd_gen_cfd(args):
    api = taiga.TaigaAPI(host=args["url"], token=args["auth_token"])
    project = api.projects.get(args["project_id"])
    tag = args["tag"]
    output_path = args["output_path"]
    target_date = None
    target_layer = None
    status_ids = None
    annotations_off = args["annotations_off"]

    # Data
    data = read_daily_cfd(output_path, tag)
    dates = data[0]
    annotations = data[1]
    annotation_layer = data[2]
    data = data[3:]

    status_ids, status_names = get_status_and_names_sorted(project)
    selected_sids = None
    if "status_ids" in args and args["status_ids"]:
        # Ids are plotted in the reversed order
        selected_sids = [int(sid) for sid in args["status_ids"].split(",")]
        selected_sids.reverse()
    else:
        selected_sids = status_ids

    selected_snames = []
    selected_data = []
    for sid in selected_sids:
        try:
            idx = status_ids.index(sid)
        except ValueError:
            print(
                "Selected US status ID {:d} not found for project {:s}!".format(
                    sid, project.name
                )
            )
            return 1
        selected_snames.append(status_names[idx])
        selected_data.append(data[idx])

    y = numpy.row_stack(tuple(selected_data))
    x = dates

    # Plotting
    fig, ax = plt.subplots()
    fig.set_size_inches(w=20.0, h=10)
    tag_str = " for {:s}".format(tag) if tag != c.TAG_MATCH_ALL else ""
    fig.suptitle("Cumulative Flow Diagram{:s}".format(tag_str))
    plt.xlabel("Week", fontsize=18)
    plt.ylabel("Number of USs", fontsize=16)
    polys = ax.stackplot(x, y)

    # X-axis, plot per week.
    mondays = WeekdayLocator(MONDAY)
    # months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
    # monthsFmt = DateFormatter("%b '%y")
    weeks = WeekdayLocator(byweekday=MONDAY, interval=1)
    # weeksFmt = DateFormatter("%W ('%y)")
    weeksFmt = DateFormatter("%W")
    ax.xaxis.set_major_locator(weeks)
    ax.xaxis.set_major_formatter(weeksFmt)
    ax.xaxis.set_minor_locator(mondays)
    ax.autoscale_view()
    # ax.grid(True)
    fig.autofmt_xdate()

    if not annotations_off:
        # Draw annotations of the data.
        bbox_props = dict(boxstyle="round4,pad=0.3", fc="white", ec="black", lw=2)
        for i, annotation in enumerate(annotations):
            if annotation != NO_ANNOTATION:
                y_coord = 0  # Calculate the Y coordnate by stacking up y values below.
                for j in range(annotation_layer[i] + 1):
                    y_coord += y[j][i]
                ax.text(
                    x[i],
                    (y_coord + 5),
                    annotation,
                    ha="center",
                    va="center",
                    rotation=30,
                    size=10,
                    bbox=bbox_props,
                )

    # Generation date string
    date_now = time.strftime("%Y-%m-%d %H:%M:%S")
    date_str = "Generated at {:s}".format(date_now)
    fig.text(0.125, 0.1, date_str)

    # Ideal pace line
    print_ideal = False
    ideal_line = None
    if ("target_date" in args and args["target_date"]) and (
        "target_layer" in args and args["target_layer"]
    ):
        print_ideal = True
        target_date = args["target_date"]
        target_date_dt = dt.datetime.strptime(target_date, "%Y-%m-%d")
        if mplotdates.date2num(target_date_dt) < mplotdates.date2num(x[0]):
            print(
                "Target date must be after the first data point stored!",
                file=sys.stderr,
            )

        target_layer = int(args["target_layer"])
        if not (0 <= target_layer < len(y)):
            print("Ideal target layer not in range!", file=sys.stderr)
            return 1

        y_ideal_start = 0
        for i in range(target_layer - 1):
            y_ideal_start += y[i][0]
        y_ideal_end = 0
        for i in range(target_layer + 1):
            y_ideal_end += y[i][-1]

        ideal_line = plt.plot(
            [x[0], target_date_dt],
            [y_ideal_start, y_ideal_end],
            color="k",
            linestyle="--",
            linewidth=3,
            label="Ideal Pace",
        )

        # Extend last known value of target layer if needed.
        if mplotdates.date2num(x[-1]) < mplotdates.date2num(target_date_dt):
            plt.hlines(
                y_ideal_end,
                x[-1],
                target_date_dt,
                colors="k",
                linestyles="--",
                linewidth=3,
            )

    # Legend
    # - Stack plot legend
    legendProxies = []
    for poly in polys:
        legendProxies.append(plt.Rectangle((0, 0), 1, 1, fc=poly.get_facecolor()[0]))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # - Ideal line legend
    if print_ideal and ideal_line:
        legendProxies.append(
            plt.Line2D(
                (0, 1),
                (0, 0),
                color=ideal_line[0].get_color(),
                linestyle=ideal_line[0].get_linestyle(),
                linewidth=ideal_line[0].get_linewidth(),
            )
        )
        selected_snames.append(ideal_line[0].get_label())

    ax.legend(
        reversed(legendProxies),
        reversed(selected_snames),
        title="Color chart",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    out_file = CFD_OUT_PNG_FMT.format(get_tag_str(tag))
    out_path = "{:s}/{:s}".format(output_path, out_file)
    plt.savefig(out_path)

    print("CFD{:s} generated at: {:s}".format(tag_str, out_path))
    return 0


@assert_args("output_path")
def cmd_gen_config_template(args):
    output_path = args["output_path"]

    config = configparser.ConfigParser()
    config["taiga"] = {
        "url": "https://api.taiga.io/",
        "auth_token": "",
    }
    config["default_values"] = {
        "project_id": "",
        "tag": "",
        "output_path": "",
        "target_date": "",
        "target_layer": "",
        "status_ids": "",
    }

    fpath = "{:s}/{:s}".format(output_path, c.CONF_FILE_NAME_FMT)
    try:
        with open(fpath, "w") as configfile:
            config.write(configfile)
    except IOError:
        print("Could not create {:s}".format(fpath), file=sys.stderr)
        return 1

    print(
        "Template created. Rename and edit it:\n$ mv {:s} {:s}".format(
            fpath, c.CONF_FILE_PATH_XDG
        )
    )
    return 0
