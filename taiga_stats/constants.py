import os

TAG_MATCH_ALL = "*"
CUST_ATTRIB_DEPENDSON_NAME = "Depends On"

CONF_FILE_PATH_XDG = os.environ["XDG_CONFIG_HOME"] + "/taiga-stats/taiga-stats.conf"
CONF_FILE_PATH = "~/.taiga-stats.conf"
CONF_FILE_NAME_FMT = "taiga-stats.conf.template"

CFD_DATA_FILE_FMT = "cfd_{:s}.dat"
