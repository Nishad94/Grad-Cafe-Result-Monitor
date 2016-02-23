# Grad-Cafe-Result-Monitor
Automatically get notified by email when there is a decision added to Grad Cafe for a university you are interested in.

# Dependencies
- Django 1.9.2
- Scrapy

# How-to Run
python manage.py runserver

# Description
Periodically[Every hour] scrapes gradcafe to check for new decisions with respect to decisions in the current database. If any user[stored in database] has saved these schools/branches as his interests, sends an email to the user.
