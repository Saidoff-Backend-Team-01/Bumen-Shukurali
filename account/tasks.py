from celery import shared_task
from django.core.mail import send_mail
from django.core.cache import cache
from random import shuffle
from django.conf import settings



def create_code(email):
    code_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    shuffle(code_list)
    code = ''.join(code_list[0:6])

    cache.set(email, code, 120)

    return code




@shared_task
def send_verification_code(email):
    subject = 'Email verification'
    code = create_code(email)
    message = f'Your code is {code}'



    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]  
    )