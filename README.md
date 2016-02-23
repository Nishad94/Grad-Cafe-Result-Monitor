# Grad-Cafe-Result-Monitor
Automatically get notified by email when there is a decision added to Grad Cafe for a university you are interested in.
Head to https://gradcafemonitor.herokuapp.com/results/ to see this web app in action.

# Dependencies
- Django 1.9.2
- Scrapy

# How-to Run
- python manage.py runserver
- python daemon.py

# Set up database and migrations for Django
- python manage.py makemigrations results
- python manage.py migrate
- python manage.py createsuperuser

# Description
Periodically[Every hour] scrapes gradcafe to check for new decisions with respect to decisions in the current database. If any user[stored in database] has saved these schools/branches as his interests, sends an email to the user.
