from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from general.models import OfficeCategory, Office, Rank, BOS, Profile, Option

class Command(BaseCommand):
    help = 'Delete the seeded dummy data from the database'

    def handle(self, *args, **kwargs):
        # Delete the created Options
        Option.objects.all().delete()

        # Delete the created Profiles
        Profile.objects.all().delete()

        # Delete the created BOS
        BOS.objects.all().delete()

        # Delete the created Offices
        Office.objects.all().delete()

        # Delete the created Office Categories
        OfficeCategory.objects.all().delete()

        # Delete the created Ranks
        Rank.objects.all().delete()

        # Delete all users except the superuser
        users = User.objects.exclude(is_superuser=True)
        user_count = users.count()
        usernames = users.values_list('username', flat=True)
        users.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted the seeded dummy data from the database'))
