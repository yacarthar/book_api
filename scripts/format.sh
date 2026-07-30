#!/bin/bash

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
isort --recursive --apply app tests
ruff format app tests