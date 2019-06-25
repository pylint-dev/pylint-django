"""
Checks that Pylint does not complain about various
methods on many-to-many relationships
"""
#  pylint: disable=missing-docstring
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


class Book(models.Model):
    name = models.CharField(max_length=100)
    good = models.BooleanField(default=False)


class Author(models.Model):
    name = models.CharField(max_length=100)
    wrote = models.ManyToManyField(Book, verbose_name="Book",
                                   related_name='books')

    def get_good_books(self):
        return self.wrote.filter(good=True)

    def is_author_of(self, book):
        return book in list(self.wrote.all())

    def wrote_how_many(self):
        return self.wrote.count()


# Custom permissions for CustomUser
USER_PERMS = ['change_customuser', 'add_customuser']


class CustomUser(AbstractUser):  # pylint: disable=model-no-explicit-unicode
    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
        app_label = "users"

    def grant_permissions(self):
        ''' Example adding permissions to User '''
        self.user_permissions.clear()
        for perm in USER_PERMS:
            perm = Permission.objects.get(codename=perm)
            self.user_permissions.add(perm)
        return self.user_permissions

    def add_permission(self, permission):
        self.user_permissions.add(permission)

    def remove_permission(self, permission):
        self.user_permissions.remove(permission)

    def set_permissions(self, permissions):
        self.user_permissions.set(permissions)

    def save(self, *args, **kwargs):
        ''' Saving while granting new permissions '''
        self.is_staff = True
        super(CustomUser, self).save()
        self.grant_permissions()
