import datetime as dt
import sys

import matplotlib

import taiga_stats.constants as c

matplotlib.use("TkAgg")  # Reference: https://stackoverflow.com/a/48374671/265508


DOT_HEADER_FMT = """digraph {:s} {{
  labelloc="t";
  //labelfontsize="40"
  label="{:s}";
  //size="7.5,10"
  ratio="compress"
  //orientation=landscape
"""


def get_tag_str(tag):
    return "" if tag == c.TAG_MATCH_ALL else tag


def get_stories_with_tag(project, tag):
    uss = project.list_user_stories()
    ret_uss = None
    if tag == c.TAG_MATCH_ALL:
        ret_uss = uss
    else:
        ret_uss = []
        for us in uss:
            if us.tags and tag in us.tags:
                ret_uss.append(us)

    if ret_uss is None or len(ret_uss) == 0:
        print(
            "Warning: no userstories matching '{:s}' was found.".format(tag),
            file=sys.stderr,
        )
        sys.exit(1)
    return ret_uss


def get_us_stauts_id_from_name(project, name):
    statuses = project.list_user_story_statuses()
    for status in statuses:
        if status.name == name:
            return status.id
    return None


def get_us_status_name_from_id(project, status_id):
    statuses = project.list_user_story_statuses()
    for status in statuses:
        if status.id == status_id:
            return status.name
    return None


def remove_closed_stories(project, uss):
    ret_uss = []
    for us in uss:
        if not us.is_closed:
            ret_uss.append(us)
    return ret_uss


def get_statuses_sorted_by_order(project):
    statuses = project.list_user_story_statuses()
    return sorted(statuses, key=lambda status: status.order)


def get_statuses_sorted_by_id(project):
    statuses = project.list_user_story_statuses()
    return sorted(statuses, key=lambda status: status.id)


def get_status_id_sorted(project):
    return [status.id for status in get_statuses_sorted_by_order(project)]


def get_status_and_names_sorted(project):
    status_ids = get_status_id_sorted(project)[::-1]
    status_names = []
    for status_id in status_ids:
        status_names.append(get_us_status_name_from_id(project, status_id))

    return status_ids, status_names


def get_dot_header(name, title):
    return DOT_HEADER_FMT.format(name, title)


def get_dot_footer():
    return "}"


def read_daily_cfd(path, tag):
    data_file = c.CFD_DATA_FILE_FMT.format(get_tag_str(tag))
    data_path = "{:s}/{:s}".format(path, data_file)
    data = []
    try:
        with open(data_path, "r") as fdata:
            row = 0
            for line in fdata:
                line = line.rstrip()
                parts = line.split("\t")
                if row == 0:
                    data = [[] for _ in range(len(parts) + 1)]
                else:
                    for col in range(len(parts)):
                        value = parts[col]
                        if col == 0:  # First col is dates
                            value = dt.datetime.strptime(value, "%Y-%m-%d")
                        elif col == 1:  # Second col is annotations
                            pass
                        else:
                            value = int(value)
                        data[col].append(value)

                row += 1
    except IOError as e:
        print(
            "Could not read {:s}, error: {:s}".format(data_path, str(e)),
            file=sys.stderr,
        )
        sys.exit(2)

    return data


class assert_args(object):
    """
    Assert that the given arguments exists.
    """

    def __init__(self, *args):
        self.needed_args = args

    def __call__(self, func):
        dec = self

        def wrapper(args):
            for arg in dec.needed_args:
                if arg not in args or args[arg] is None:
                    print(
                        "Required argument ''{:s}' was not supplied on commandline or set in config file.".format(
                            arg
                        )
                    )
                    return 1
            func(args)

        return wrapper
