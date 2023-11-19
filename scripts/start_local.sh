#!/bin/bash

export PLATFORM_ENVIRONMENT_TYPE=local
uvicorn app.main:app --reload