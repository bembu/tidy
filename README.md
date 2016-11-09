# Tidy

A neat and tidy Flask-powered blog engine

![](https://raw.githubusercontent.com/bembu/tidy/master/images/preview.png)

#### Currently there is a support for:
* Easy to use, clean style
* User Accounts
    * Two user roles: admin and normal user. Both can create and edit posts, but only admin can manage users and posts (i.e. delete)
* Blog posts are written in Markdown. All symbols supported via flask-markdown library
* RESTful URLS with easily readable post title slugs
* Users can upload thumbnail images to their blog posts
* Authors can tag posts into different categories. USers can view posts by tags.
* Simple, working pagination

#### Possible additions in the future:
* About Me -page
* Comments (probably Disqus)
* Account management (i.e. password resets)

## Initial Steps

There are a few steps you need to take in order to get the blog to work on a development server

1. Install a virtual environment for Python 2.7, activate it and install required libraries indicated in requirements.txt file `pip install -r /path/to/requirements.txt`

2. Initialize the database
    * `python db_create.py` to create the database
    * `python db_migrate.py` to create a migration
    * `python db_upgrade.py` to upgrade the database version

3. You might want to edit the config.py file, especially change the 'dummy' secret key

3. `python run.py` to run the app on a dev server.
