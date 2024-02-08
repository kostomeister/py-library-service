#!/bin/sh




# Perform Django database migrations
python manage.py wait_for_db
python manage.py makemigrations user
python manage.py migrate
python manage.py makemigrations book_service
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
nohup python notifications_bot.py &


# Start Django development server
python manage.py runserver 0.0.0.0:8000
