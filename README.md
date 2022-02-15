# Taiga Stats - Your Taiga Statistics Tool [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Scrum%20and%20Kanban%20masters;%20generate%20statistics%20from%20your%20Taiga.io%20projects%20with%20this%20python%20tool&url=https://github.com/erikw/jekyll-glossary_tooltip&via=erik_westrup&hashtags=taiga,scrum,kanban,statistics)
[![PyPI version](https://badge.fury.io/py/taiga-stats.svg)](https://badge.fury.io/py/taiga-stats)
[![Downloads](https://pepy.tech/badge/taiga-stats)](https://pepy.tech/project/taiga-stats)
[![Documentation Status](https://readthedocs.org/projects/taiga-stats/badge/?version=latest)](https://taiga-stats.readthedocs.io/en/latest/?badge=latest)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/taiga-stats)](#)
[![Travis Build Status](https://img.shields.io/travis/com/erikw/taiga-stats/master?logo=travis)](https://app.travis-ci.com/github/erikw/taiga-stats)
[![Lint Code Base](https://github.com/erikw/taiga-stats/actions/workflows/linter.yml/badge.svg)](https://github.com/erikw/taiga-stats/actions/workflows/linter.yml)
[![SLOC](https://img.shields.io/tokei/lines/github/erikw/taiga-stats)](#)
[![License](https://img.shields.io/pypi/l/taiga-stats)](https://github.com/erikw/taiga-stats/blob/master/LICENSE)
[![OSS Lifecycle](https://img.shields.io/osslifecycle/erikw/taiga-stats)](https://github.com/Netflix/osstracker)

This is a script for all you Scrum||Kanban masters out there who use Taiga and are interested in visualizing progress and generate some automated statistics and graphs.

[Taiga](https://taiga.io/) is an Open Source virtual Scrum and Kanban board that is popular for managing projects and work. We use a physical whiteboard at work but I mirror the status of stories in Taiga so that I can collect some statistics and generate diagrams and graphs using this tool I wrote.

# Features
```console
$ taiga-stats --help
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

# Terminology
* *US* - User Story
* *CFD* - Cumulative Flow Diagram

## Cumulative Flow Diagram
From a [CFD](http://brodzinski.com/2013/07/cumulative-flow-diagram.html) a lot of interesting insights about your team's progress [can be found](http://paulklipp.com/images/Interpreting_a_Cumulative_Flow_Diagram.jpg). However I'm not found of repetitive work like counting and entering numbers in an Excel sheet. This had to be automated! Therefore I deiced to write this script to save data on a daily basis with a cron job and a function for generating this diagram. This diagram can the be put on a TV visible in the hallways.


This is an example diagram generated from [mock data](https://github.com/erikw/taiga-stats/tree/master/sample_data/cfd_example.dat):

![Example CFD](https://raw.githubusercontent.com/erikw/taiga-stats/master/img/cfd_example.png)

Textual annotations can be put in the plot by manually editing the `.dat file`.


Also a target date for the project deadline can be specified. Then a line will be drawn showing the ideal work pace towards this date, as seen below where the target finish date is in week 46.

![Example CFD with ideal pace](https://raw.githubusercontent.com/erikw/taiga-stats/master/img/cfd_example_ideal_pace.png)


To save the data and generate the diagram each working day I have this cronjob:

```console
$ crontab -l | grep taiga
0 18 * * 1-5            $HOME/bin/taiga-stats-cron.sh
```

and the script `taiga-stats-cron.sh`:

```bash
#!/usr/bin/env sh

taiga-stats store_daily --tag some_feature_tag
taiga-stats cfd --tag some_feature_tag
```

## User Story Dependency Graph
Some stories requires other to be completed before they can be started. I thought it would be handy if you could keep track of these dependencies in Taiga but simply writing for each US a list of other stories that this story depends on. Then from this information a [.dot file](https://github.com/erikw/taiga-stats/tree/master/sample_data/dependencies_example.dot) can be generated that should how you user stories depends on each other. This graph is very useful for work planning i.e. what to start with and how much parallelization is possible and at what stages.

![US Dependency Graph](https://raw.githubusercontent.com/erikw/taiga-stats/master/img/dependencies_example.png)

The stories that are marked as Done in Taiga have a green color in the graph.


### How to set up the dependency feature
First create a new custom filed in taiga named `Depends On` under Settings > Attributes > Custom Fields:

![Custom Field](https://raw.githubusercontent.com/erikw/taiga-stats/master/img/taiga_custom_field.png)


Then go to your User Stories and enter some dependencies as demonstrated below.

![US dependency](https://raw.githubusercontent.com/erikw/taiga-stats/master/img/us_depends_on.png)


Then run the script and generate a PNG file.


```console
$ taiga-stats deps_dot
$ dot -T png -o ./dependencies.png ./dependencies.dot
```


# Setup

## Installation
Make sure to use a supported python version. See the key `python` in the section `tool.poetry.dependencies` at [pyproject.toml](https://github.com/erikw/taiga-stats/blob/master/pyproject.toml).

```console
$ pip install taiga-stats
$ taiga-stats -h
```

If you use [pipx](https://pypi.org/project/pipx/) to install, you must specify a supported and locally available python version like:

```console
$ pipx install --python python3.9 taiga-stats
```

To use this tool, you need to supply
* `--url` to your taiga server e.g. `https://api.taiga.io/`
* `--auth-token` that you need to obtain according to the [official instructions](https://docs.taiga.io/api.html#_authentication).

It's recommended to put these 2 values in the below described `taiga-stats.conf` file for easier usage of this tool!

## Config file
It is tedious to have to specify the server URL and the authentication token every time. Also you typically work with some project at a time and would like to have default values for the project to use and maybe which tag to filter on. You can generate a configuration file to set these default values.

```console
$ taiga-stats config_template
$ mv ./taiga.conf.template ~/.taiga-stats.conf
$ vi ~/.taiga-stats.conf
```


# Development
* Make sure to `$ poetry shell` before using tools like pyright LSP, so that it can find the installed dependency modules
* Reference for how to structure a python project: https://realpython.com/pypi-publish-python-package/

## Setup from Git
* Clone this git
```console
$ git clone https://github.com/erikw/taiga-stats.git && cd $(basename "$_" .git)
```
* Install Poetry
```console
$ pip install poetry
```

* Numpy install issues as of 2021-10-31
* `$ poetry install` did not work with Numpy on macOS. Solution from https://github.com/python-poetry/poetry/issues/3196#issuecomment-769753478
```console
$ pyenv local 3.9.7
$ poetry env use 3.9.7
$ poetry config experimental.new-installer false
$ poetry install
```

* Install project dependencies
```console
$ poetry install
```
* Now taiga-stats should work!
```console
$ poetry run taiga-stats -h
$ # or
$ bin/taiga-stats.sh
```
* To install locally:
```console
$ poetry build
$ pip install dist/taiga_stats-*.whl
```

# Development
## Documentation generation
```console
$ poetry run mkdocs serve
$ poetry run mkdocs build
```

but `bin/gen_docs.sh` will take care of all that plus more!

# Releasing
```console
$ bin/gen_docs.sh
$ vi CHANGELOG.md
$ poetry version minor && ver="v$(poetry version -s)"
$ git commit -am "Bump version to $ver" && git tag $ver && git push --atomic origin master $ver
$ poetry publish --build
```
