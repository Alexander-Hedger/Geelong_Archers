from django.db import models
from django.contrib.postgres.fields import ArrayField
from accounts.models import Account


class MemberEvents(models.Model):
    member = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_index=True)
    link = models.CharField(max_length=200)
    event_name = models.CharField(max_length=100)
    club = models.CharField(max_length=100)
    discipline = models.CharField(max_length=10)
    date = models.DateField()
    day = models.IntegerField()
    flight = models.IntegerField()
    archer_class = models.CharField(max_length=20)
    division = models.CharField(max_length=20)
    archery_round = models.CharField(max_length=40)
    score = models.IntegerField()
    rating = models.FloatField()
    awards = ArrayField(ArrayField(models.CharField(max_length=60)))
    total_awards = models.IntegerField()


class Awards(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='awards/', blank=True)

    def __str__(self):
        return self.name


class MemberAwards(models.Model):
    member = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_index=True)
    award = models.ForeignKey(Awards, on_delete=models.PROTECT)
    date_recieved = models.DateField()


class MemberAvailableAwards(models.Model):
    member = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_index=True)
    award = models.ForeignKey(Awards, on_delete=models.PROTECT)


class MemberClassification(models.Model):
    member = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    rank = models.IntegerField()
    discipline = models.CharField(max_length=20)
    archer_class = models.CharField(max_length=20)
    division = models.CharField(max_length=30)
    classification = models.CharField(max_length=30)
    score_count = models.IntegerField()
    classification_id = models.ForeignKey(Awards, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class MemberClassificationAnnual(models.Model):
    member = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    rank = models.IntegerField()
    discipline = models.CharField(max_length=20)
    archer_class = models.CharField(max_length=20)
    division = models.CharField(max_length=30)
    classification = models.CharField(max_length=30)
    score_count = models.IntegerField()
    year = models.IntegerField()
    classification_id = models.ForeignKey(Awards, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
