from django.db import models

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
        
