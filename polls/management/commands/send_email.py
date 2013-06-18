from django.core.management.base import BaseCommand, CommandError
import django.core.mail as dm
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import get_connection

from polls.models import Participant, EmailMessage, Notification

from optparse import make_option

import sys
import os
import csv

from string import Template

from collections import defaultdict

CONSOLE_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SMTP_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FILEBASED_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

class Command(BaseCommand):
    help = """Sends participant notifications.
If no recipients file is given, recipients are taken from the command line,
unless the -a option is passed, in which case messages are sent
to all participants currently in the the database, or the -i option is passed,
in which case messages are sent to the recipients contained in the input file.
    """
    args = '<user1 user2 ...>'
    option_list = BaseCommand.option_list + (
        make_option('-t',
                    '--title',
                    action='store',
                    type='string',
                    dest='title',
                    help='message title',
                ),                
        make_option('-a',
                    '--all',
                    action='store_true',
                    dest='all',
                    help='send notification to all recipients',
                ),        
        make_option('-i',
                    '--input',
                    action='store',
                    type='string',
                    dest='input_file',
                    help='set recipients file',
                    ),
        make_option('-c',
                    '--console_back_end',
                    action='store_true',
                    dest='console_back_end',
                    help='use console backend',
                ),
        make_option('-b',
                    '--file_back_end',
                    action='store',
                    dest='file_back_end',
                    type='string',
                    help='use file backend',
                ),                
    )

    def make_message(self, participant, mapping, message_template):
        mapping.update({
            'unique_id': participant.unique_id,
            })
        if message_template is not None:
            message = message_template.safe_substitute(mapping)
        else:
            message = ""
        return message
                
    def send_email(self, args, options):
        if options['file_back_end']:
            backend = get_connection(FILEBASED_BACKEND,
                                     file_path=options['file_back_end'])
        elif options['console_back_end']:
            backend = get_connection(CONSOLE_BACKEND)
        else:
            backend = get_connection(SMTP_BACKEND)
        try:
            message = EmailMessage.objects.get(title=options['title'])
        except ObjectDoesNotExist:
            return
        message_template = Template(message.body)
        if options['all']:
            participants = Participant.objects.exclude(
                notification__email_message_id=message.id)
        elif options['input_file']:
            with open(options['input_file'], 'r') as participants_file:
                emails = [x.rstrip() for x in participants_file.readlines()]
                participants = Participant.objects.filter(
                    email__in=emails)
        else:
            participants = Participant.objects.filter(email__in=args)
        
        for participant in participants:
            body = self.make_message(participant,
                                     {},
                                     message_template)
            msg = dm.EmailMessage(message.subject_header,
                                  body,
                                  message.from_header,
                                  [participant.email],
                                  connection=backend)
            for attachment in message.attachments.all():
                msg.attach(attachment.filename, attachment.data,
                           attachment.mimetype)
            msg.send()
            if not options['file_back_end'] and not options['console_back_end']:
                notification = Notification(participant=participant,
                                            email_message=message)
                notification.save()
            
    def handle(self, *args, **options):
        self.send_email(args, options)
        
        
        
