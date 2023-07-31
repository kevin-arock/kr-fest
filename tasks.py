# ct_site/tasks.py
from __future__ import absolute_import, unicode_literals
import django
django.setup()
import os
import uuid
import subprocess
from celery import shared_task
import pandas as pd
from django.core.mail import EmailMessage
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE
from .models import UserReg
from .models import Post


@shared_task
def send_mail_task(id):
    # Get the data from the User model
    post = Post.objects.get(id=id)
    fest = post.title
    users = UserReg.objects.all()

    # Create the Excel spreadsheet using pandas
     # Filter data for faculty (sors='Faculty')
    faculty_users = users.filter(sors__contains='staff',event__contains=fest)

    # Filter data for students (sors='Student')
    student_users = users.filter(sors__contains='student',event__contains=fest)

    filename = f'users_data_{uuid.uuid4()}.xlsx'

    # Create the Excel spreadsheet using pandas
    with pd.ExcelWriter(filename) as writer:
        # Sheet1 - Faculty
        faculty_dataframe = pd.DataFrame(list(faculty_users.values(
            'name', 'email', 'cllgname', 'event', 'fromcllg', 'sors'
        )))
        faculty_dataframe.rename(
            columns={
                'name': 'Name',
                'email': 'Email',
                'cllgname': 'Fest Held At',
                'event': 'Fest Name',
                'fromcllg': 'From',
                'sors': 'Designation'
            },
            inplace=True
        )
        faculty_dataframe.insert(0, 'S.No', range(1, len(faculty_dataframe) + 1))
        faculty_dataframe.to_excel(writer, index=False, sheet_name='Sheet1')

        # Sheet2 - Students
        student_dataframe = pd.DataFrame(list(student_users.values(
            'name', 'email', 'cllgname', 'event', 'fromcllg', 'sors'
        )))
        student_dataframe.rename(
            columns={
                'name': 'Name',
                'email': 'Email',
                'cllgname': 'Fest Held At',
                'event': 'Fest Name',
                'fromcllg': 'From',
                'sors': 'Designation'
            },
            inplace=True
        )
        student_dataframe.insert(0, 'S.No', range(1, len(student_dataframe) + 1))
        student_dataframe.to_excel(writer, index=False, sheet_name='Sheet2')

    # Create the email message with attachment
    email_message = EmailMessage(
        subject='Fest Registration Detais',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['2002hariraj@gmail.com'],  # Replace with recipient email address
    )

    with open(filename, 'rb') as file:
        email_message.attach(filename, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Send the email
    email_message.send()

    # Delete the temporary Excel file
    os.remove(filename)

    return 'Email sent with attachment.'


@shared_task
def send_mail_task_ce(id):
    # Get the data from the User model
    post = Post.objects.get(id=id)
    fest = post.title
    users = UserReg.objects.all()

    # Create the Excel spreadsheet using pandas
     # Filter data for faculty (sors='Faculty')
    faculty_users = users.filter(sors__contains='staff',event__contains=fest)

    # Filter data for students (sors='Student')
    student_users = users.filter(sors__contains='student',event__contains=fest)

    filename = f'users_data_{uuid.uuid4()}.xlsx'

    # Create the Excel spreadsheet using pandas
    with pd.ExcelWriter(filename) as writer:
        # Sheet1 - Faculty
        faculty_dataframe = pd.DataFrame(list(faculty_users.values(
            'name', 'email', 'cllgname', 'event', 'fromcllg', 'sors'
        )))
        faculty_dataframe.rename(
            columns={
                'name': 'Name',
                'email': 'Email',
                'cllgname': 'Fest Held At',
                'event': 'Fest Name',
                'fromcllg': 'From',
                'sors': 'Designation'
            },
            inplace=True
        )
        faculty_dataframe.insert(0, 'S.No', range(1, len(faculty_dataframe) + 1))
        faculty_dataframe.to_excel(writer, index=False, sheet_name='Sheet1')

        # Sheet2 - Students
        student_dataframe = pd.DataFrame(list(student_users.values(
            'name', 'email', 'cllgname', 'event', 'fromcllg', 'sors'
        )))
        student_dataframe.rename(
            columns={
                'name': 'Name',
                'email': 'Email',
                'cllgname': 'Fest Held At',
                'event': 'Fest Name',
                'fromcllg': 'From',
                'sors': 'Designation'
            },
            inplace=True
        )
        student_dataframe.insert(0, 'S.No', range(1, len(student_dataframe) + 1))
        student_dataframe.to_excel(writer, index=False, sheet_name='Sheet2')

    # Create the email message with attachment
    email_message = EmailMessage(
        subject='Fest Registration Detais',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['2002hariraj@gmail.com'], 
    )

    with open(filename, 'rb') as file:
        email_message.attach(filename, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Send the email
    email_message.send()

    # Delete the temporary Excel file
    os.remove(filename)

    return 'Email sent with attachment.'
    
@shared_task
def send_mail_task_mk(id):
    # Get the data from the User model
    post = Post.objects.get(id=id)
    fest = post.title
    users = UserReg.objects.all()

    # Create the Excel spreadsheet using pandas
     # Filter data for faculty (sors='Faculty')
    faculty_users = users.filter(sors__contains='staff',event__contains=fest)

    # Filter data for students (sors='Student')
    student_users = users.filter(sors__contains='student',event__contains=fest)

    filename = f'users_data_{uuid.uuid4()}.xlsx'

    # Create the Excel spreadsheet using pandas
    with pd.ExcelWriter(filename) as writer:
        # Sheet1 - Faculty
        faculty_dataframe = pd.DataFrame(list(faculty_users.values(
            'name', 'email', 'cllgname', 'event', 'fromcllg', 'sors'
        )))
        faculty_dataframe.rename(
            columns={
                'name': 'Name',
                'email': 'Email',
                'cllgname': 'Fest Held At',
                'event': 'Fest Name',
                'fromcllg': 'From',
                'sors': 'Designation'
            },
            inplace=True
        )
        faculty_dataframe.insert(0, 'S.No', range(1, len(faculty_dataframe) + 1))
        faculty_dataframe.to_excel(writer, index=False, sheet_name='Sheet1')

        # Sheet2 - Students
        student_dataframe = pd.DataFrame(list(student_users.values(
            'name', 'email', 'cllgname', 'event', 'fromcllg', 'sors'
        )))
        student_dataframe.rename(
            columns={
                'name': 'Name',
                'email': 'Email',
                'cllgname': 'Fest Held At',
                'event': 'Fest Name',
                'fromcllg': 'From',
                'sors': 'Designation'
            },
            inplace=True
        )
        student_dataframe.insert(0, 'S.No', range(1, len(student_dataframe) + 1))
        student_dataframe.to_excel(writer, index=False, sheet_name='Sheet2')

    # Create the email message with attachment
    email_message = EmailMessage(
        subject='Fest Registration Detais',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['bhuvanshankar0@gmail.com'],  # Replace with recipient email address
    )

    with open(filename, 'rb') as file:
        email_message.attach(filename, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Send the email
    email_message.send()

    # Delete the temporary Excel file
    os.remove(filename)

    return 'Email sent with attachment.'


'''
restart_celery()
def restart_celery():
    # Restart Celery using subprocess module
    # Replace 'celery -A your_project_name worker' with the command to start Celery in your project
    subprocess.Popen(['celery', '-A', 'ct_site', 'worker', '--poolsolo','-l','info'])
'''