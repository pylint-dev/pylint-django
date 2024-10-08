# pylint: disable=missing-docstring, wildcard-import, unused-wildcard-import

from django.contrib.auth.models import *  # [imported-auth-user] # noqa: F403
from django.db import models


class PullRequest(models.Model):
    author = models.ForeignKey("auth.User", models.CASCADE)  # [hard-coded-auth-user]
