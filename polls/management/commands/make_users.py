#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
import polls
from polls.models import Participant, Institution, School, Department

from django.contrib.auth.models import User

from django.db import transaction

from optparse import make_option

import os
import csv

class Command(BaseCommand):
    help = """Initialises user data.

If no input file is given, reads users.csv from fixtures."""
    option_list = BaseCommand.option_list + (
        make_option('-i',
                    '--input',
                    action='store',
                    type='string',
                    dest='input_file',
                    help='set users file',
                ),
    )
    pth = os.path.abspath(polls.__path__[0])

    @transaction.commit_on_success
    def create_users(self, users_file_path=None):
        if users_file_path is None:
            users_file_path = os.path.join(Command.pth,
                                           'fixtures',
                                           'users.csv')
        with open(users_file_path, 'rb') as users_file:
            u_reader = csv.reader(users_file)
            for i, row in enumerate(u_reader):
                if i == 0:
                    continue
                row = [item.strip() for item in row]
                email = row[-1].lower()
                (first_name, last_name, institution_name,
                 school_name, department_name, email) = row
                (institution, created) = Institution.objects.get_or_create(
                    name=institution_name)
                if created:
                    institution.save()
                (school, created) = School.objects.get_or_create(
                    name=school_name)
                if created:
                    school.save()
                (department, created) = Department.objects.get_or_create(
                    name=department_name)
                if created:
                    department.save()
                base_username = email.split('@')[0].lower()[0:28]
                username = base_username            
                j = 2
                while User.objects.filter(username=username).exists():
                    username = "{}_{}".format(base_username, i)
                    j += 1
                user = User.objects.create_user(username=username,
                                                email=email)
                unique_id = Participant.generate_unique_id()
                user.first_name = first_name.decode('utf-8')[0:30]
                user.last_name = last_name.decode('utf-8')[0:30]
                participant = Participant()
                participant.first_name = first_name
                participant.last_name = last_name
                participant.institution = institution
                participant.school = school
                participant.department = department
                participant.unique_id = unique_id
                user.save()
                participant.user = user
                participant.save()
                if i % 100 == 0:
                    self.stdout.write("\r{}".format(i), ending='')
                    self.stdout.flush()
                self.stdout.write("")
                        
    def handle(self, *args, **options):
        self.create_users(options['input_file'])

        
        
