from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from django.urls import reverse
from django.core.cache import cache


class Person(models.Model):
    """
    Person who posts Notice on the noticeboard
    In case we want to extend user with additional fields in the future

    For now o2o linked to User
    """
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f'<Person {self.user.username}#{self.user.id}>'


class Category(models.Model):
    """
    Notice Category
    """

    title = models.TextField()

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Category #{self.id}>'


class Notice(models.Model):
    """
    Main content unit on noticeboard
    """
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = QuillField()
    timestamp = models.DateTimeField('Timestamp ', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.content.plain

    def __repr__(self):
        return f'<Notice #{self.id}>'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'notice#{self.pk}')

    def get_absolute_url(self):
        return reverse('core:notice_detail', args=[str(self.id)])


# class NoticeCategory(models.Model):
#     """
#     m2m link between Notice and Category
#     """
#     notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Rejoinder(models.Model):
    """
    A reply to Notice

    I've just learned the word 'rejoinder' meaning cunning or sarcastic reply
    ¯\_(ツ)_/¯
    """
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    content = models.TextField()
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField('Timestamp ', auto_now_add=True)

    def __str__(self):
        return self.content

    def __repr__(self):
        return f'<Rejoinder #{self.id}>'
