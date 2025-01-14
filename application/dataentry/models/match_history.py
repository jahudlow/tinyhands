from django.db import models
from django.contrib.postgres.fields import JSONField

from .person import Person
from .master_person import MasterPerson, MatchType
from accounts.models import Account

class MatchAction(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

class MatchHistory(models.Model):
    master1 = models.ForeignKey(MasterPerson, related_name='masterHistory1')
    master2 = models.ForeignKey(MasterPerson, related_name='masterHistory2', null=True)
    person = models.ForeignKey(Person, null=True)
    notes = models.TextField(blank=True)
    match_type = models.ForeignKey(MatchType, null=True)
    action = models.ForeignKey(MatchAction)    # create MP, create match , remove, merge, type change
    timestamp = models.DateTimeField(auto_now_add=True)
    matched_by = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    match_results = JSONField(null=True)