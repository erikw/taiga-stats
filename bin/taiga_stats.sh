#!/usr/bin/env bash
# Simple wrapper


DIR=$(dirname "$0")
cd $DIR/..
poetry run taiga_stats $*
