# Taiga Statistics Tool

This is a script for all you "Kanban masters" who use Taiga and are interested in visualizing progress and generate some automated statistics and graphs.

[Taiga](https://taiga.io/) is an Open Source virtual Scrum and Kanban board that is popular for managing projects and work. We use a physical whiteboard at work but I mirror the status of stories in Taiga so that I can collect some statistics and generate diagrams and graphs using this tool I wrote.

# Features

```console
$ taiga-stats --help
usage: taiga-stats [-h] [--url URL] [--auth-token AUTH_TOKEN]
                   {config_template,list_projects,list_us_statuses,burnup,store_daily,cfd,deps_dot_nodes,deps_dot}
                   ...

Taiga statistic tool. Default values for many options can be set config file;
see the command 'config_template'.

positional arguments:
  {config_template,list_projects,list_us_statuses,burnup,store_daily,cfd,deps_dot_nodes,deps_dot}
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
  --url URL             URL to Taiga server.
  --auth-token AUTH_TOKEN
                        Authentication token. Instructions on how to get one
                        is found at https://taigaio.github.io/taiga-
                        doc/dist/api.html#_authentication
```

## Cumulative Flow Diagram

From a [CFD](http://brodzinski.com/2013/07/cumulative-flow-diagram.html) a lot of interesting insights about your team's progress [can be found](http://paulklipp.com/images/Interpreting_a_Cumulative_Flow_Diagram.jpg). However I'm not found of repetitive work like counting and entering numbers in an Excel sheet. This had to be automated! Therefore I deiced to write this script to save data on a daily basis with a cron job and a function for generating this diagram. This diagram can the be put on a TV visible in the hallways.


This is an example diagram generated from [mock data](sample_data/cfd_example.dat):

![Example CFD](img/cfd_example.png)

Textual annotations can be put in the plot by manually editing the `.dat file`.


Also a target date for the project deadline can be specified. Then a line will be drawn showing the ideal work pace towards this date, as seen below where the target finish date is in week 46.

![Example CFD with ideal pace](img/cfd_example_ideal_pace.png)


To save the data and generate the diagram each working day I have this cronjob:

```console
$ crontab -l | grep taiga
0 18 * * 1-5            $HOME/bin/taiga-stats_cron.sh
```

and the script `taiga-stats_cron.sh`:

```bash
#!/usr/bin/env sh

source $HOME/dev/virtualenvs/py3env/bin/activate
cd $HOME/dev/taiga-stats

./taiga-stats store_daily --tag some_feature_tag
./taiga-stats cfd --tag some_feature_tag
```

## User Story Dependency Graph

Some stories requires other to be completed before they can be started. I thought it would be handy if you could keep track of these dependencies in Taiga but simply writing for each US a list of other stories that this story depends on. Then from this information a [.dot file](sample_data/dependencies_example.dot) can be generated that should how you user stories depends on each other. This graph is very useful for work planning i.e. what to start with and how much parallelization is possible and at what stages.

![US Dependency Graph](img/dependencies_example.png)

The stories that are marked as Done in Taiga have a green color in the graph.


### How to set up the dependency feature

First create a new custom filed in taiga named `Depends On` under Settings > Attributes > Custom Fields:

![Custom Field](img/taiga_custom_field.png)


Then go to your User Stories and enter some dependencies as demonstrated below.

![US dependency](img/us_depends_on.png)


Then run the script and generate a png file.


```console
$ taiga-stats deps_dot
$ dot -T png -o ./dependencies.png ./dependencies.dot
```


# Setup

## Virtual environment (optional)

It is recommended to use virtual environment to not pollute your system.

```console
$ sudo apt-get install python3-dev
$ cd some/dev/dir
$ virtualenv -p /usr/bin/python3 py3env
$ source py3env/bin/activate
```

## Dependencies

Use either

pip (recommended)

```console
$ pip install -r requirements.txt
```

or setuptools

```console
$ python setup.py install
```

## Taiga-stats

```console
$ git clone https://github.com/erikw/taiga-stats.git
$ cd taiga-stats
$ ./taiga-stats -h
```

## Config file

It is tedious to have to specify the server URL and the authentication token everytime. Also you typically work with some project at a time and would like to have default values for the project to use and maybe which tag to filter on. You can genearte a configuration file to set these default values.


```console
$ taiga-stats config_template
$ mv ./taiga.conf.template ~/.taiga-stats.conf
$ vi ~/.taiga-stats.conf
```
