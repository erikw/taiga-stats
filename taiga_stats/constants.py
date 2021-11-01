import os

TAG_MATCH_ALL = '*'
CUST_ATTRIB_DEPENDSON_NAME = 'Depends On'

CONF_FILE_PATH_XDG = os.environ["XDG_CONFIG_HOME"] + '/taiga_stats/taiga_stats.conf'
CONF_FILE_PATH = '~/.taiga_stats.conf'
CONF_FILE_NAME_FMT = 'taiga_stats.conf.template'

CFD_DATA_FILE_FMT = 'cfd_{:s}.dat'
