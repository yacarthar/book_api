set SQLALCHEMY_SILENCE_UBER_WARNING=1
set PLATFORM_ENVIRONMENT_TYPE=test
pytest --cov=app --tb=short -vv -s -p no:loggin  tests --cov-report term-missing