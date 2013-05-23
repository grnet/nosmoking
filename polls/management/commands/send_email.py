from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import get_connection

import poll

from poll.models import UserProfile
from django.contrib.auth.models import User

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
    help = """Sends user invitations.
If no users file is given, users are taken from the command line,
unless the -a option is passed, in which case messages are sent
to ill users currently in the the database, or the -i option is passed,
in which case messages are sent to the users contained in the input file.

If the -p option is passed, it must be the location of a file
output by the make_users command; otherwise, it assumes that the file
is called user_pass.cvs and is found in the fixtures directory.

If the -m option is passed, it must be the location of a message template;
otherwise it assumes that the file is called message_template.txt and is
found in the fixtures directory.
    """
    pth = os.path.abspath(poll.__path__[0])
    args = '<user1 user2 ...>'
    option_list = BaseCommand.option_list + (        
        make_option('-a',
                    '--all',
                    action='store_true',
                    dest='all',
                    help='send invitation to all users',
                ),        
        make_option('-i',
                    '--input',
                    action='store',
                    type='string',
                    dest='input_file',
                    help='set users file',
                    ),
        make_option('-s',
                    '--subject',
                    action='store',
                    type='string',
                    dest='subject',
                    default='no subject',
                    help='set email subject',
                ),
        make_option('-f',
                    '--from',
                    action='store',
                    type='string',
                    dest='from',
                    default='no-reply',
                    help='set from field',
                ),
        make_option('-m',
                    '--message',
                    action='store',
                    type='string',
                    dest='message_file',
                    default=os.path.join(pth,
                                         'fixtures',
                                         'mail_template.txt'),
                    help='set message contents',
                ),
        make_option('-p',
                    '--passwords',
                    action='store',
                    type='string',
                    default=os.path.join(pth,
                                         'fixtures',
                                         'user_pass.csv'),
                    dest='passwords_file',
                    help='set passwords file',
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

    def make_invite(self, user, mapping, message_template):
        mapping.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        })
        try:
            up = user.user_profile            
            project = up.project
            mapping.update({
                'project_acronym': project.acronym,
                'project_name': project.name,
            })
            instrument = project.instrument
            mapping['instrument_name'] = instrument.name
            institute = project.institute
            mapping['institute_name'] = institute.name
        except ObjectDoesNotExist:
            pass
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
        
        passwords = defaultdict(lambda: '')
        if os.path.isfile(options['passwords_file']):
            with open(options['passwords_file'], 'r') as passwords_file:
                p_reader = csv.reader(passwords_file)
                for row in p_reader:
                    passwords[row[-2]] = row[-1]
        message_template = None
        if os.path.isfile(options['message_file']):
            with open(options['message_file'], 'r') as message_file:
                message_template = Template(message_file.read().decode('utf-8'))
        if options['all']:
            users = User.objects.all()
        elif options['input_file']:
            with open(options['input_file'], 'r') as usernames_file:
                usernames = [x.rstrip() for x in usernames_file.readlines()]
                users = User.objects.filter(username__in=usernames)
        else:
            users = User.objects.filter(username__in=args)
        for user in users:
            message = self.make_invite(user,
                                       {'password': passwords[user.username]},
                                       message_template)
            send_mail(options['subject'], message,
                      options['from'],
                      [user.email], fail_silently=False,
                      connection=backend)
            
    def handle(self, *args, **options):
        self.send_email(args, options)
        
        
        
