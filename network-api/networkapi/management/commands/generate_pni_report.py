from urllib.parse import urlparse
import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings

from networkapi.buyersguide.models import Product

class Command(BaseCommand):
    help = 'Generate statistical data about privacynotincluded activity, for internal' \
           ' dashboards and update a DB connected to data studio'

    def add_arguments(self, parser):
        pass

    def setup_db_connection(self):
        STATS_DB = urlparse(settings.PNI_STATS_DB_URL)
        return psycopg2.connect(
            host=STATS_DB.hostname,
            port=STATS_DB.port,
            user=STATS_DB.username,
            password=STATS_DB.password,
            database=STATS_DB.path[1:]
        )

    def fetch_stats(self):
        stats = []
        for product in Product.objects.all():
            votes = product.votes

            creepiness_votes = 0
            for bucket in votes['creepiness']['vote_breakdown']:
                creepiness_votes += votes['creepiness']['vote_breakdown'][bucket]

            stats.append({
                'id': product.id,
                'product': product.name,
                'creepiness': votes['creepiness']['average'],
                'creepiness_votes': creepiness_votes,
                'wouldbuy': votes['confidence']['1'],
                'wouldnotbuy': votes['confidence']['0']
            })

        return stats


    def handle(self, *args, **options):
        connection = None
        try:
            connection = self.setup_db_connection()
            cursor = connection.cursor()
            stats = self.fetch_stats()
            print(stats)
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection closed')
