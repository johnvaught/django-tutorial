import datetime

from django.db import models
from django.utils import timezone
from hashids import Hashids

HASHIDS_SALT = '7b41003547267ca733ce723739c3712479657a0806440f29'
hashids = Hashids(HASHIDS_SALT, min_length=8)


def get_pk_from_hashid(hashid):
    return hashids.decode(hashid)[0]


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"

    def get_hashid_from_pk(self):
        return hashids.encode(self.pk)

    def total_votes(self):
        count = 0
        choices = Choice.objects.filter(question=self.id)
        for choice in choices:
            count += choice.votes
        return count

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
