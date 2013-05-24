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

    def __unicode__(self):
        return self.choice_text

    class Meta:
        ordering = ['position']

class Institution(models.Model):
    name = models.CharField(max_length=100, unique=True)

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
        
class Participant(models.Model):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    institution = models.ForeignKey(Institution)
    school = models.ForeignKey(School, null=True)
    department = models.ForeignKey(Department)
    unique_id = models.CharField(max_length=100)

    @classmethod
    def generate_unique_id(cls):
        unique_id = ''.join(random.choice(string.ascii_lowercase +
                                          string.digits)
                            for x in range(20))
        while Participant.objects.filter(unique_id=unique_id).exists():
            unique_id = ''.join(random.choice(string.ascii_lowercase +
                                              string.digits)
                                for x in range(50))
        return unique_id

class Response(models.Model):

    participant = models.ForeignKey(Participant)
    choice = models.ForeignKey(Choice)
    created_at = models.DateTimeField(auto_now_add=True)    
    modified_at = models.DateTimeField(auto_now=True)
