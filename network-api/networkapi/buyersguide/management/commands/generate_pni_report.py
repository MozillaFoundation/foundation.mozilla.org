import psycopg2
import re

from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.conf import settings

from networkapi.buyersguide.models import Product

LOCALE_REGEX = '/([a-z]{2}(?:-[A-Z]{2})?/)'


class Command(BaseCommand):
    # TODO: Look into whether or not this management command is still needed.
    # TODO: Create a follow up ticket for this.
    help = 'Generate statistical data about privacynotincluded activity, for internal' \
           ' dashboards and update a DB connected to data studio'

    @staticmethod
    def setup_db_connection():
        STATS_DB = urlparse(settings.PNI_STATS_DB_URL)
        return psycopg2.connect(
            host=STATS_DB.hostname,
            port=STATS_DB.port,
            user=STATS_DB.username,
            password=STATS_DB.password,
            database=STATS_DB.path[1:]
        )

    @staticmethod
    def fetch_stats():
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

    @staticmethod
    def form_product_string(data):
        return '({id}, \'{name}\', {value}, {votes}, {yes}, {no})'.format(
            id=data['id'],
            name=data['product'],
            value=data['creepiness'],
            votes=data['creepiness_votes'],
            yes=data['would_buy'],
            no=data['would_not_buy']
        )

    @staticmethod
    def form_comment_string(data):
        return '(\'{url}\', \'{title}\', {total_comments})'.format(
            url=data['url'],
            title=data['title'],
            total_comments=data['totalCommentCount']
        )

    @staticmethod
    def dedupe_comments(comments):
        cleaned_comments = dict()
        for comment in comments:
            url = re.sub(LOCALE_REGEX, '/', comment['url'])

            # Filter out the records created before we fixed og title meta tags
            if comment['title'] == 'privacy not included':
                continue

            elif url in cleaned_comments:
                cleaned_comments[url]['totalCommentCount'] += comment['totalCommentCount']

            else:
                cleaned_comments[url] = comment
                cleaned_comments[url]['url'] = url

        return list(cleaned_comments.values())

    @staticmethod
    def generate_insert_values(data, formstring):
        retval = ''
        for i in range(len(data)):
            retval += formstring(data[i])
            if i != len(data) - 1:
                retval += ', '

        return retval

    def handle(self, *args, **options):

        if not settings.PNI_STATS_DB_URL:
            print('You must set PNI_STATS_DB_URL to run this task')
            return

        connection = None

        try:
            print('Fetching Product data')
            stats = self.fetch_stats()

            print('Generating Upsert Query for product data')
            sql_products = 'INSERT INTO product_stats\n' \
                           f'VALUES { self.generate_insert_values(stats, self.form_product_string) }\n' \
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

            print('Executing Upsert Queries')
            cursor.execute(sql_products)
            print('Done!')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection closed')
