# Tidy

A neat and tidy Flask-powered blog engine

## Initial Steps

There are a few steps you need to take in order to get the blog to work on a development server

1. Install a virtual environment for Python 2.7, activate it and install required libraries indicated in requirements.txt file `pip install -r /path/to/requirements.txt`

2. Initialize the database
    * `python db_create.py` to create the database
    * `python db_migrate.py` to create a migration
    * `python db_upgrade.py` to upgrade the database version

3. `python run.py` to run the app on a dev server.
