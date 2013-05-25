from django.contrib import admin
from polls.models import *

class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
        
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['subject']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(EmailMessage)
admin.site.register(Notification)
admin.site.register(Institution)
admin.site.register(Response)
admin.site.register(Sign)

