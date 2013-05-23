from django.db import models

from django.contrib.auth.models import User

import random
import string

random.seed()

class Poll(models.Model):
    subject = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.subject
    
class Question(models.Model):
    poll = models.ForeignKey(Poll)
    question_text = models.CharField(max_length=200)
    position = models.IntegerField(default=0)    

    def __unicode__(self):
        return self.question_text

    class Meta:
        ordering = ['position']
    
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    position = models.IntegerField(default=0)    
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text

    class Meta:
        ordering = ['position']

class Institution(models.Model):
    name = models.CharField(max_length=100)

class School(models.Model):
    name = models.CharField(max_length=100)

class Department(models.Model):
    name = models.CharField(max_length=100)
        
class Participant(models.Model):
    
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    institution = models.ForeignKey(Institution)
    school = models.ForeignKey(School)
    department = models.ForeignKey(Department)
    unique_id = models.CharField(max_length=100)

    @classmethod
    def generate_unique_id(cls):
        unique_id = ''.join(random.choice(string.ascii_lowercase +
                                          string.digits)
                            for x in range(50))
        while Participant.objects.filter(unique_id=unique_id).exists():
            unique_id = ''.join(random.choice(string.ascii_lowercase +
                                              string.digits)
                                for x in range(50))
        return unique_id
