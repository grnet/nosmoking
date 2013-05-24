#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
import polls
from polls.models import Participant, Institution, School, Department

from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction

from optparse import make_option

import os
import csv

class Command(BaseCommand):
    help = """Initialises user data.

If no input file is given, reads the corresponding file from fixtures.
The files in fixtures should be:
    users.csv
    institutions.csv
    schools.csv
    departments.csv
"""
    option_list = BaseCommand.option_list + (
        make_option('-i',
                    '--input',
                    action='store',
                    type='string',
                    dest='input_file',
                    help='set users file',
                ),
        make_option('-n',
                    '--institutions',
                    action='store_true',
                    dest='institutions',
                    help='create institutions',
            ),
        make_option('-s',
                    '--schools',
                    action='store_true',
                    dest='schools',
                    help='create schools',
                ),
        make_option('-d',
                    '--departments',
                    action='store_true',
                    dest='departments',
                    help='create departments',
                ),                        
    )
    pth = os.path.abspath(polls.__path__[0])

    def file_reader(self, input_file_path):
        with open(input_file_path, 'rb') as users_file:
            u_reader = csv.reader(users_file)
            for i, row in enumerate(u_reader):
                if i == 0:
                    continue
                row = [item.strip() for item in row]
                yield(row)
                if i % 100 == 0:
                    self.stdout.write("\r{}".format(i), ending='')
                    self.stdout.flush()
            self.stdout.write("")
            self.stdout.write("{}".format(i))                    
    
    @transaction.commit_on_success
    def create_entities(self, class_name, input_file):
        for i, row in enumerate(self.file_reader(input_file)):
            name = row[0]
            cls = eval(class_name)
            cls.objects.get_or_create(name=name)
            
    def create_users(self, input_file):
        for i, row in enumerate(self.file_reader(input_file)):        
            (first_name, last_name, institution_name,
             school_name, department_name, email) = row
            participant = Participant()            
            try:
                participant.institution = Institution.objects.get(
                    name=institution_name)
            except ObjectDoesNotExist:
                pass
            try:
                participant.school = School.objects.get(name=school_name)
            except ObjectDoesNotExist:
                pass
            try:
                participant.department = Department.objects.get(
                    name=department_name)
            except ObjectDoesNotExist:
                pass
            unique_id = Participant.generate_unique_id()
            participant.first_name = first_name
            participant.last_name = last_name
            participant.unique_id = unique_id
            participant.email = email
            participant.save()
            if i % 100 == 0:
                self.stdout.write("\r{}".format(i), ending='')
                self.stdout.flush()
        self.stdout.write("")
        self.stdout.write("{}".format(i))                    
                        
    def handle(self, *args, **options):
        input_file_path = options['input_file']
        if options['institutions']:
            if input_file_path is None:
                input_file_path = os.path.join(Command.pth,
                                               'fixtures',
                                               'institutions.csv')            
            self.create_entities('Institution', input_file_path)
        elif options['schools']:
            if input_file_path is None:
                input_file_path = os.path.join(Command.pth,
                                               'fixtures',
                                               'schools.csv')            
                self.create_entities('School', input_file_path)
        elif options['departments']:
            if input_file_path is None:
                input_file_path = os.path.join(Command.pth,
                                               'fixtures',
                                               'departments.csv')            
                self.create_entities('Department', input_file_path)
        else:
            if input_file_path is None:
                input_file_path = os.path.join(Command.pth,
                                               'fixtures',
                                               'users.csv')
            self.create_users(input_file_path)

        
        
