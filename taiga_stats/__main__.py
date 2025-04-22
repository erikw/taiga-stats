# Entry point when called as a module
# $ python -m taiga_stats

import sys

import taiga_stats.constants as c
from taiga_stats import commands, config, parse_args

COMMAND2FUNC = {
    "burnup": commands.cmd_print_burnup_data,
    "cfd": commands.cmd_gen_cfd,
    "config_template": commands.cmd_gen_config_template,
    "deps_dot_nodes": commands.cmd_print_us_in_dep_format,
    "deps_dot": commands.cmd_us_in_dep_format_dot,
    "list_projects": commands.cmd_list_projects,
    "list_us_statuses": commands.cmd_list_us_statuses,
    "store_daily": commands.cmd_store_daily_stats,
    "points_sum": commands.cmd_points_sum,
}


def main():
    args = parse_args.parse_args()
    (
        cnf_url,
        cnf_auth_token,
        cnf_project_id,
        cnf_tag,
        cnf_output_path,
        cnf_target_date,
        cnf_target_layer,
        cnf_status_ids,
        cnf_annotations_off,
        cnf_print_tags,
        cnf_print_points,
    ) = config.read_config()

    args["url"] = args["url"] if "url" in args and args["url"] else cnf_url
    args["auth_token"] = args["auth_token"] if "auth_token" in args and args["auth_token"] else cnf_auth_token if cnf_auth_token else None
    args["project_id"] = args["project_id"] if "project_id" in args and args["project_id"] else cnf_project_id if cnf_project_id else None
    args["tag"] = args["tag"] if "tag" in args and args["tag"] else cnf_tag if cnf_tag else c.TAG_MATCH_ALL
    args["output_path"] = args["output_path"] if "output_path" in args and args["output_path"] else cnf_output_path if cnf_output_path else "."
    args["target_date"] = (
        args["target_date_and_layer"][0] if "target_date_and_layer" in args and args["target_date_and_layer"] else cnf_target_date if cnf_target_date else None
    )
    args["target_layer"] = (
        args["target_date_and_layer"][1]
        if "target_date_and_layer" in args and args["target_date_and_layer"]
        else cnf_target_layer
        if cnf_target_layer
        else None
    )
    args["status_ids"] = args["status_ids"] if "status_ids" in args and args["status_ids"] else cnf_status_ids if cnf_status_ids else None
    args["annotations_off"] = (
        args["annotations_off"]
        if "annotations_off" in args and args["annotations_off"] is not None
        else cnf_annotations_off
        if cnf_annotations_off is not None
        else False
    )
    args["print_tags"] = (
        args["print_tags"]
        if "print_tags" in args and args["print_tags"] is not None and args["print_tags"]
        else cnf_print_tags
        if cnf_print_tags is not None
        else False
    )
    args["print_points"] = (
        args["print_points"]
        if "print_points" in args and args["print_points"] is not None and args["print_points"]
        else cnf_print_points
        if cnf_print_points is not None
        else False
    )

    if args["command"] not in COMMAND2FUNC:
        print("Misconfiguration for argparse: subcommand not mapped to a function")
        return 1
    command_func = COMMAND2FUNC[args["command"]]
    args.pop("command")

    return command_func(args)


if __name__ == "__main__":
    sys.exit(main())
