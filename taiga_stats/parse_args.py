import argparse

import taiga_stats
import taiga_stats.constants as c


def parse_args():
    tool_desc = "Taiga statistic tool. Default values for many options can be set config file; see the command 'config_template'."
    at_help = "Authentication token. Instructions on how to get one is found at {:s}"
    tdal_help = (
        "Specify the targeted finish date for the project and a line for the ideal work pace will be drawn. "
        'Also specify which layer to draw the line to. e;g; "2015-10-21 3"'
    )
    ao_help = "Turn off user user defined annotations. Default is on."
    sd_help = "Store the current state of a project on file so that the CFD command can generate a diagram with this data."
    b_help = "Print burn(up|down) statistics. Typically used for entering in an Excel sheet or such that plots a burnup."
    cfd_help = "Generate a Cumulative Flow Diagram from stored data."
    dd_help = (
        "Print US in .dot file format with dependencies too! Create a custom attribute for User Stories named '{:s}' by "
        "going to Settings>Attributes>Custom Fields. Then go to a User Story and put in a comma separated list of stories that "
        "this story depends on e.g. '#123,#456'."
    )

    parser = argparse.ArgumentParser(prog="taiga-stats", description=tool_desc, epilog="Support: please go to https://github.com/erikw/taiga-stats/issues")

    # General options
    parser.add_argument("-v", "--version", action="version", version=taiga_stats.__version__)
    parser.add_argument("--url", help="URL to Taiga server.")
    parser.add_argument(
        "--auth-token",
        help=at_help.format("https://docs.taiga.io/api.html#_authentication"),
    )

    # Common options to commands
    opt_tag = argparse.ArgumentParser(add_help=False)
    opt_tag.add_argument(
        "--tag",
        help="Taiga tag to use. Defaults is to not filter which can also be achieved by giving the value '*' to this option.",
    )

    opt_project_id = argparse.ArgumentParser(add_help=False)
    opt_project_id.add_argument("--project-id", help="Project ID in Taiga to get data from.")

    opt_output_path = argparse.ArgumentParser(add_help=False)
    opt_output_path.add_argument(
        "--output-path",
        help="Store daily statistics for later usage with the 'cfd' command.",
    )

    opt_target_date = argparse.ArgumentParser(add_help=False)
    opt_target_date.add_argument("--target-date-and-layer", nargs=2, help=tdal_help)

    opt_status_ids = argparse.ArgumentParser(add_help=False)
    opt_status_ids.add_argument(
        "--status-ids",
        help="A comma separated and sorted list of User Story status IDs to use.",
    )

    opt_annotations_off = argparse.ArgumentParser(add_help=False)
    opt_annotations_off.add_argument("--annotations-off", dest="annotations_off", action="store_true", help=ao_help)

    opt_print_tags = argparse.ArgumentParser(add_help=False)
    opt_print_tags.add_argument(
        "--print-tags",
        dest="print_tags",
        action="store_true",
        help="Print a US's tags in the nodes.",
    )

    opt_print_points = argparse.ArgumentParser(add_help=False)
    opt_print_points.add_argument(
        "--print-points",
        dest="print_points",
        action="store_true",
        help="Print a US's total points in the nodes.",
    )

    # Commands
    subparsers = parser.add_subparsers(
        help="Commands. Run $(taiga-stats <command> -h) for more info about a command.",
        dest="command",
    )
    subparsers.required = True

    subparsers.add_parser(
        "config_template",
        parents=[opt_output_path],
        help="Generate a template configuration file.",
    )
    subparsers.add_parser(
        "list_projects",
        help="List all found project IDs and names on the server that you have access to read.",
    )
    subparsers.add_parser(
        "list_us_statuses",
        parents=[opt_project_id],
        help="List all the ID and names of User Story statuses.",
    )
    subparsers.add_parser("burnup", parents=[opt_project_id, opt_tag, opt_status_ids], help=b_help)
    subparsers.add_parser("store_daily", parents=[opt_project_id, opt_tag, opt_output_path], help=sd_help)
    subparsers.add_parser(
        "points_sum",
        parents=[opt_project_id, opt_tag, opt_status_ids],
        help="Print out the sum of points in User Story statuses.",
    )
    subparsers.add_parser(
        "cfd",
        parents=[
            opt_project_id,
            opt_tag,
            opt_output_path,
            opt_target_date,
            opt_status_ids,
            opt_annotations_off,
        ],
        help=cfd_help,
    )
    subparsers.add_parser(
        "deps_dot_nodes",
        parents=[opt_project_id, opt_tag, opt_status_ids],
        help="Print User Story nodes in .dot file format.",
    )
    subparsers.add_parser(
        "deps_dot",
        parents=[
            opt_project_id,
            opt_tag,
            opt_output_path,
            opt_status_ids,
            opt_print_tags,
            opt_print_points,
        ],
        help=dd_help.format(c.CUST_ATTRIB_DEPENDSON_NAME),
    )

    return vars(parser.parse_args())
