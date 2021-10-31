import os

# TODO only keep constants that are used across multiple modules here.
################# Constants #####################
CFD_DATA_FILE_FMT='cfd_{:s}.dat'
CFD_OUT_PNG_FMT='cfd_{:s}.png'
NO_ANNOTATION='NONE'
TAG_MATCH_ALL='*'
CUST_ATTRIB_DEPENDSON_NAME='Depends On'

CONF_FILE_PATH_XDG=os.environ["XDG_CONFIG_HOME"] + '/taiga-stats/taiga-stats.conf'
CONF_FILE_PATH='~/.taiga-stats.conf'
CONF_FILE_NAME_FMT='taiga.conf.template'

DEPS_DOT_FILE_FMT='dependencies_{:s}'

DOT_HEADER_FMT = """digraph {:s} {{
  labelloc="t";
  //labelfontsize="40"
  label="{:s}";
  //size="7.5,10"
  ratio="compress"
  //orientation=landscape
"""
