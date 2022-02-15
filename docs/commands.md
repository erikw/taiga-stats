# Commands
```console
usage: taiga-stats [-h] [-v] [--url URL] [--auth-token AUTH_TOKEN]
                   {config_template,list_projects,list_us_statuses,burnup,store_daily,points_sum,cfd,deps_dot_nodes,deps_dot}
                   ...

Taiga statistic tool. Default values for many options can be set config file;
see the command 'config_template'.

positional arguments:
  {config_template,list_projects,list_us_statuses,burnup,store_daily,points_sum,cfd,deps_dot_nodes,deps_dot}
                        Commands. Run $(taiga-stats <command> -h) for more
                        info about a command.
    config_template     Generate a template configuration file.
    list_projects       List all found project IDs and names on the server
                        that you have access to read.
    list_us_statuses    List all the ID and names of User Story statuses.
    burnup              Print burn(up|down) statistics. Typically used for
                        entering in an Excel sheet or such that plots a
                        burnup.
    store_daily         Store the current state of a project on file so that
                        the CFD command can generate a diagram with this data.
    points_sum          Print out the sum of points in User Story statuses.
    cfd                 Generate a Cumulative Flow Diagram from stored data.
    deps_dot_nodes      Print User Story nodes in .dot file format.
    deps_dot            Print US in .dot file format with dependencies too!
                        Create a custom attribute for User Stories named
                        'Depends On' by going to Settings>Attributes>Custom
                        Fields. Then go to a User Story and put in a comma
                        separated list of stories that this story depends on
                        e.g. '#123,#456'.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --url URL             URL to Taiga server.
  --auth-token AUTH_TOKEN
                        Authentication token. Instructions on how to get one
                        is found at
                        https://docs.taiga.io/api.html#_authentication

Support: please go to https://github.com/erikw/taiga-stats/issues
```

Full documentation at [github.com/erikw/taiga-stats](https://github.com/erikw/taiga-stats).
