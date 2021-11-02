import configparser
import os

import taiga_stats.constants as c


def read_config():
    url = None
    auth_token = None
    project_id = None
    tag = None
    output_path = None
    target_date = None
    target_layer = None
    status_ids = None
    annotations_off = None
    print_tags = None
    print_points = None

    config = configparser.ConfigParser()
    conf_xdg = os.path.expanduser(c.CONF_FILE_PATH_XDG)
    conf_home = os.path.expanduser(c.CONF_FILE_PATH)
    if os.path.isfile(conf_xdg):
        config.read(conf_xdg)
    else:
        config.read(conf_home)

    if "taiga" in config:
        taiga = config["taiga"]
        if "url" in taiga:
            url = taiga["url"]
        if "auth_token" in taiga:
            auth_token = taiga["auth_token"]

    if "default_values" in config:
        def_values = config["default_values"]
        if "project_id" in def_values:
            project_id = def_values["project_id"]
            if project_id:
                project_id = int(project_id)
        if "tag" in def_values:
            tag = def_values["tag"]
        if "output_path" in def_values:
            output_path = def_values["output_path"]
        if "target_date" in def_values:
            target_date = def_values["target_date"]
        if "target_layer" in def_values:
            target_layer = def_values["target_layer"]
        if "status_ids" in def_values:
            status_ids = def_values["status_ids"]
        if "annotations_off" in def_values:
            annotations_off = def_values["annotations_off"]
        if "print_tags" in def_values:
            print_tags = def_values["print_tags"]
        if "print_points" in def_values:
            print_points = def_values["print_points"]

    return (
        url,
        auth_token,
        project_id,
        tag,
        output_path,
        target_date,
        target_layer,
        status_ids,
        annotations_off,
        print_tags,
        print_points,
    )
