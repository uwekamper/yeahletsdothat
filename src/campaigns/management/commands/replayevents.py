# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from campaigns.models import ReadModel, BaseEvent
from campaigns.projectors import handle_event
from django.db import IntegrityError, transaction, connection


class Command(BaseCommand):
    args = ''
    help = 'Drops all read models from the database'

    def handle(self, *args, **options):
        with transaction.atomic():
            for sub_class in ReadModel.__subclasses__():
                self.stdout.write('Removing {}'.format(sub_class) )
                db_table = sub_class._meta.db_table
                cursor = connection.cursor()
                try:
                    cursor.execute('DELETE FROM {}'.format(db_table))
                finally:
                    cursor.close()

        self.stdout.write('Calling syncdb ...')
        # call_command('syncdb', interactive=False)

        for event in BaseEvent.objects.all():
            self.stdout.write(str(event))
            handle_event(event)


            # try:
            #     poll = Poll.objects.get(pk=int(poll_id))
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)
            #
            # poll.opened = False
            # poll.save()

            # self.stdout.write('Successfully closed poll "%s"' % poll_id)