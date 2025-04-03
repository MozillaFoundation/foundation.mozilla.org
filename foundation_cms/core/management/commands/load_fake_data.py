from django.core.management.base import BaseCommand

import foundation_cms.core.factories as core_factory

# import foundation_cms.blog.factories as blog_factory


class Command(BaseCommand):
    help = "Creates random data for the site."

    print("Start Generating Site Data...")

    def create_pages(self):
        print("Create a homepage.")
        core_factory.create_homepage()

        # print("Create a blog with blog posts.")
        # blog_factory.create_blog_with_posts()

    def handle(self, **options):
        self.create_pages()
