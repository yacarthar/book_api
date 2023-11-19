#!/bin/bash

export SQLALCHEMY_SILENCE_UBER_WARNING=1
export PLATFORM_ENVIRONMENT_TYPE=test
pytest --cov=app --tb=short -vv -s -p no:loggin  tests --cov-report term-missing