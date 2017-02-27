from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seeds the database with minimum data so that the app can be used'

    def handle(self, *args, **options):
        self.stdout.write('[*] Starting command\n')
        from sentence_split import init_db

        for username, user_dict in init_db.USERS.iteritems():
            user = User(username=username,
                        email=user_dict['email'],
                        is_superuser=True,
                        is_staff=True,
                        first_name=user_dict['first_name'],
                        last_name=user_dict['last_name'])

            self.stdout.write('[*] Creating user `%s`\n' % str(user))

            user.set_password(user_dict['password'])
            self.stdout.write('[*] Password set for user: %s \n' %
                              user.username)

            try:
                user.save()
                self.stdout.write('[*] User `%s` saved\n' % user.username)
            except Exception as e:
                self.stdout.write('[!] User `%s` could not be saved (%s)\n' %
                                  (user.username, str(e)))
