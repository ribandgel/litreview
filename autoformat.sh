#! /bin/sh

BASEDIR=$( dirname `readlink -f $0` )
cd $BASEDIR/..

autoflake --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys \
  --recursive --in-place litreview

isort litreview

flake8 --ignore E203,E501,W503 litreview

black --line-length=100 --exclude litreview/base/migrations \
  litreview \
  $@
