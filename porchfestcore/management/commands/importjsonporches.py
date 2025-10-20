# blog/management/commands/import_wp_posts.py
import json
from django.core.management.base    import BaseCommand
from django.contrib.auth.models     import User
from porchfestcore.models           import Porch
from django.utils.dateparse         import parse_datetime
from datetime                       import datetime
from django.contrib.gis.geos        import Point

class Command(BaseCommand):
    help = 'Import WordPress posts from JSON'

    def handle(self, *args, **options):
        with open('porches.json', 'r') as f:
            posts = json.load(f)
        for wp_post in posts:
            created_at = datetime.strptime(wp_post['date'], "%Y-%m-%d %H:%M:%S")
            print(created_at)

            location = Point(float(wp_post["longitude"]), float(wp_post["latitude"]), srid=4326)

            Porch.objects.create(
                name=wp_post["title"],
                description=wp_post["description"],
                street_address=wp_post["porch_address"],
                original_created_at=created_at,
                coordinates=location,
            )

        self.stdout.write(self.style.SUCCESS(f"Imported {len(posts)} posts!"))