from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from .models import Person, Notice, Rejoinder


@receiver(user_signed_up, dispatch_uid='associate_person_signal')
def associate_person(request, user, **kwargs):
    """
    Create Person when User signs up
    """
    person = Person.objects.create(user=user)


@receiver(post_save, sender=Rejoinder)
def notify_notice_author(sender, instance: Rejoinder, **kwargs):
    """
    Notify author of Notice when new rejoinder appears
    """
    notice_author = instance.notice.author
    email = notice_author.user.email
    print(notice_author, email)



