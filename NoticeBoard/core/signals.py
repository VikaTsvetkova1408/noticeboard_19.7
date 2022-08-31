from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.template.loader import get_template
from datetime import datetime, timedelta
from .models import Person, Notice, Rejoinder
from .scheduler import scheduler


@receiver(user_signed_up, dispatch_uid='associate_person_signal')
def associate_person(request, user, **kwargs):
    """
    Create Person when User signs up
    """
    person = Person.objects.create(user=user)


def send_notify_email(email, notice_id):
    ...


@receiver(post_save, sender=Rejoinder)
def notify_notice_author(sender, instance: Rejoinder, **kwargs):
    """
    Notify author of Notice when new rejoinder appears
    """
    notice = instance.notice
    notice_author = notice.author
    email = notice_author.user.email
    scheduler.add_job(send_notify_email,
                      'date',
                      run_date=datetime.now() + timedelta(seconds=10),
                      args=[email, notice.id])

