import os

# TODO only keep constants that are used across multiple modules here.
TAG_MATCH_ALL='*'
CUST_ATTRIB_DEPENDSON_NAME='Depends On'

CONF_FILE_PATH_XDG=os.environ["XDG_CONFIG_HOME"] + '/taiga-stats/taiga-stats.conf'
CONF_FILE_PATH='~/.taiga-stats.conf'
CONF_FILE_NAME_FMT='taiga.conf.template'
