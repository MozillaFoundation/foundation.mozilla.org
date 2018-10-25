import psycopg2
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.conf import settings

from networkapi.buyersguide.models import Product


class Command(BaseCommand):
    help = 'Generate statistical data about privacynotincluded activity, for internal' \
           ' dashboards and update a DB connected to data studio'

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
                'would_buy': votes['confidence']['1'],
                'would_not_buy': votes['confidence']['0']
            })

        return stats

    def generate_insert_values(self, stats):
        retval = ''
        for index, p_data in enumerate(stats):
            retval += f'({ p_data["id"] }, \'{ p_data["product"] }\', { p_data["creepiness"] }, ' \
                      f'{ p_data["creepiness_votes"] }, { p_data["would_buy"] } , { p_data["would_not_buy"] })'
            if index != len(stats) - 1:
                retval += ', '

        return retval

    def handle(self, *args, **options):
        connection = None
        try:
            print('Fetching Product data')
            stats = self.fetch_stats()

            print('Generating Upsert Query')
            sql = 'INSERT INTO public.product_stats\n' \
                  f' VALUES { self.generate_insert_values(stats) }\n' \
                  'ON CONFLICT (id) DO UPDATE\n' \
                  'SET product_name = EXCLUDED.product_name,\n' \
                  'creepiness = EXCLUDED.creepiness,\n' \
                  'creepiness_votes = EXCLUDED.creepiness_votes,\n' \
                  'would_buy = EXCLUDED.would_buy,\n' \
                  'would_not_buy = EXCLUDED.would_not_buy'

            print('Opening connection to DB')
            connection = self.setup_db_connection()
            connection.set_session(autocommit=True)
            cursor = connection.cursor()

            print('Executing Upsert')
            cursor.execute(sql)
            print('Done!')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if connection is not None:
                connection.close()
                print('Database connection closed')
