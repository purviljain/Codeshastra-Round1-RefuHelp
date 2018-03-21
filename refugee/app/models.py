from django.db import models
from django.contrib.auth.models import User
import datetime


class NGO(models.Model):
    user = models.OneToOneField(User, related_name="ngo", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    international = models.BooleanField(default=False)
    ngo_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


# Creating a custom path for storing the user photos
# Example : /MEDIA_ROOT/photos/1234567890/abc.jpg
def path(instance, filename):
    return 'photos/{0}'.format(filename)


# Creating a custom path for storing the user photos
# Example : /MEDIA_ROOT/photos/1234567890/abc.jpg
def passport(instance, filename):
    return 'passport/{0}'.format(filename)


class Refugee(models.Model):
    refugee = models.OneToOneField(User, on_delete=models.CASCADE, related_name="refugee")
    name = models.CharField(max_length=100)
    ngo = models.ForeignKey(NGO, blank=True, null=True, on_delete=models.SET_NULL, related_name="refugees")
    country = models.CharField(max_length=50)
    photo = models.FileField(blank=True, upload_to=path)
    bio = models.CharField(max_length=200, blank=True)
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    mobileNo = models.CharField(max_length=50, blank=True)
    age = models.IntegerField(blank=True)
    passport = models.FileField(blank=True, upload_to=passport)
    passport_id = models.CharField(max_length=50, blank=True, null=True)
    registered_on = models.DateField(("Date"), default=datetime.date.today, blank=True)

    def __str__(self):
        return str(self.refugee.username)


class Notification(models.Model):
    askedBy = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="notif_ngo")
    message = models.CharField(max_length=300)

    def __str__(self):
        return str(self.message)


class NgoPetition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='ngo_petitions')

    def __str__(self):
        return self.title


class NgoPetitionVote(models.Model):
    petition = models.ForeignKey(NgoPetition, on_delete=models.CASCADE, related_name='ngo_petition_votes')
    voter = models.EmailField()
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.petition.title + " -- " + self.voter


class Help(models.Model):
    asker = models.ForeignKey(Refugee, on_delete=models.CASCADE, related_name="help")
    askto = models.ForeignKey(NGO, on_delete=models.SET_NULL, null=True, related_name="req")
    helpof = models.CharField(max_length=100)
    PRIORITY = (
        ("Very High", "Very High"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    )
    urgency = models.CharField(max_length=50, choices=PRIORITY)
    description = models.CharField(max_length=1000, blank=True)
    asked_on = models.DateField(("Date"), default=datetime.date.today)

    def __str__(self):
        return str(self.help.helpof)


class Event(models.Model):
    startedBy = models.ForeignKey(NGO, on_delete=models.SET_NULL, null=True, related_name="eventngo")
    reason = models.CharField(max_length=1000)
    date = models.DateTimeField()
    location = models.CharField(max_length=1000)


class RefugeePetition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    refugee = models.ForeignKey(Refugee, on_delete=models.CASCADE, related_name='refugee_petitions')

    def __str__(self):
        return self.title


class RefugeePetitionVote(models.Model):
    petition = models.ForeignKey(RefugeePetition, on_delete=models.CASCADE, related_name='refugee_petition_votes')
    voter = models.EmailField()
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.petition.title + ' -- ' + self.voter
