from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Generate authentication tokens for all users that do not have one'

    def handle(self, *args, **options):
        users_without_token = 0
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                users_without_token += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully generated token for user "{user.username}"')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal tokens generated: {users_without_token}')
        )
