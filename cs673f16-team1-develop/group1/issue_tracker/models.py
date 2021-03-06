from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from requirements.models.project import Project

#imports for the use of tokens -DG
#See: http://cheng.logdown.com/posts/2015/10/27/how-to-use-django-rest-frameworks-token-based-authentication

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


OPEN_STATUSES = (
    ('Open-New', 'New',),
    ('Open-Assigned', 'Assigned',),
    ('Open-Accepted', 'Accepted',),
)

CLOSED_STATUSES = (
    ('Closed-Fixed', 'Fixed',),
    ('Closed-Verified', 'Verified',),
    ('Closed-Working as Intended', 'Working as Intended',),
    ('Closed-Obsolete', 'Obsolete',),
    ('Closed-Duplicate', 'Duplicate',),
)

STATUSES = (OPEN_STATUSES + CLOSED_STATUSES)

TYPES = (
    ('Bug', 'Bug',),
    ('Feature', 'Feature Request',),
    ('Internal Cleanup', 'Internal Cleanup',),
)

PRIORITIES = (
    ('High', 'High',),
    ('Medium', 'Medium',),
    ('Low', 'Low',),
)


class Issue(models.Model):
    """Issue"""

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    issue_type = models.CharField(max_length=20, choices=TYPES)
    status = models.CharField(max_length=20, default='new', choices=STATUSES)
    priority = models.CharField(max_length=20, choices=PRIORITIES)

    # Project
    project = models.ForeignKey(Project, null=True)

    # Dates
    submitted_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)
    closed_date = models.DateTimeField(null=True, editable=False)

    # Users
    reporter = models.ForeignKey(User, related_name='reporter', null=True)
    assignee = models.ForeignKey(User, related_name='assignee', blank=True, null=True)
    verifier = models.ForeignKey(User, related_name='verifier', blank=True, null=True)

    class Meta(object):
        ordering = ['id']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'pk': self.pk})


class IssueComment(models.Model):
    comment = models.TextField(max_length=2000)
    issue_id = models.ForeignKey(Issue, related_name='comments', blank=False, null=False) #order them by issue PK -DG
    date = models.DateTimeField(auto_now_add=True, editable=False)
    poster = models.ForeignKey(User, related_name='comments', blank=True, null=True)
    is_comment = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'pk': self.issue_id})


def get_all_issues():
    return Issue.objects.all()
