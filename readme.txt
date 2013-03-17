To get running:

copy Androkon/androkon/androkon/settings.py.template to just settings.py, and edit lines 15, 121, and 73 to change db file, template folder and static folder locations respectively.
Point the template folder at Androkon/templates, static at Androkon/static, and the db file where ever you want, it'll be created there.

cd to Androkon/androkon and run python manage.py syncdb to create the database.

run python manage.py runserver to start server, then point browser at localhost:8000 to view

If you are ian: 
    change DEBUG to False on line 3
    change SECRET_KEY on line 88 of settings.py, otherwise it doesn't matter for just testing
