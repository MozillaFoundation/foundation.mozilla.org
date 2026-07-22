from collections import Counter
from datetime import timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from wagtail.models import Locale, Page, Site

from foundation_cms.base.models.abstract_base_page import Author, Topic
from foundation_cms.core.models import GeneralPage

DEFAULT_COUNT = 16
DEFAULT_KEYWORD = "SEARCH_FILTER_TEST"
DEFAULT_AUTHOR_NAME = "Search QA Author"

SECTIONS = (
    ("what-we-do", "What We Do"),
    ("research", "Research"),
    ("press-release", "Press Release"),
    ("event", "Event"),
)

TOPICS = (
    ("privacy", "Privacy"),
    ("artificial-intelligence", "Artificial Intelligence"),
    ("open-web", "Open Web"),
    ("security", "Security"),
)


class Command(BaseCommand):
    help = (
        "Create deterministic published pages for testing search filters, topics, sorting, and pagination. "
        "Existing pages prefixed by the selected keyword are replaced."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=DEFAULT_COUNT,
            help=f"Pages to create across the search sections (default: {DEFAULT_COUNT}).",
        )
        parser.add_argument(
            "--keyword",
            type=str,
            default=DEFAULT_KEYWORD,
            help=f"Keyword included in generated titles and descriptions (default: {DEFAULT_KEYWORD}).",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete pages prefixed by the selected keyword without recreating them.",
        )
        parser.add_argument(
            "--update-index",
            action="store_true",
            help="Run Wagtail update_index after creation (useful for external search backends).",
        )

    def _get_site_and_locale(self):
        site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
        if not site:
            raise CommandError("No default Wagtail Site found; run load_redesign_data first.")

        locale = site.root_page.locale if site.root_page_id else Locale.get_default()
        return site, locale

    def _get_or_create_section_root(self, site, locale, slug, title):
        section_root = site.root_page.get_children().filter(locale=locale, slug=slug).first()
        if section_root:
            if not section_root.live:
                section_root.save_revision().publish()
            return Page.objects.get(pk=section_root.pk)

        section_root = (
            Page.objects.live()
            .descendant_of(site.root_page, inclusive=False)
            .filter(locale=locale, slug=slug)
            .order_by("depth", "path", "id")
            .first()
        )
        if section_root:
            return section_root

        section_root = Page(title=title, slug=slug, locale=locale)
        site.root_page.add_child(instance=section_root)
        section_root.save_revision().publish()
        self.stdout.write(f'Created missing search section root "{title}".')
        return section_root

    def _get_or_create_topics(self):
        topics = []
        for slug, name in TOPICS:
            topic, _ = Topic.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": "Shared topic used by generated search QA pages.",
                },
            )
            topics.append(topic)
        return topics

    def _delete_pages(self, keyword):
        keyword_slug = slugify(keyword) or "search-filter-test"
        pages = GeneralPage.objects.filter(
            author__name=DEFAULT_AUTHOR_NAME,
            title__startswith=f"{keyword} ",
            slug__startswith=f"{keyword_slug}-",
            search_description__startswith=f"{keyword} local QA result for ",
        )
        count = pages.count()
        if count:
            pages.delete()
        return count

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        keyword = (options["keyword"] or DEFAULT_KEYWORD).strip()

        if count <= 0:
            raise CommandError("--count must be > 0")
        if not keyword:
            raise CommandError("--keyword must be a non-empty string")

        deleted = self._delete_pages(keyword)
        if options["delete"]:
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} generated search test pages."))
            return

        if deleted:
            self.stdout.write(f"Replacing {deleted} existing search test pages...")

        site, locale = self._get_site_and_locale()
        section_roots = {slug: self._get_or_create_section_root(site, locale, slug, title) for slug, title in SECTIONS}
        topics = self._get_or_create_topics()
        author, _ = Author.objects.get_or_create(
            name=DEFAULT_AUTHOR_NAME,
            defaults={"bio": "Author used by generated search QA pages."},
        )

        section_counts = Counter()
        now = timezone.now()
        keyword_slug = slugify(keyword) or "search-filter-test"

        for index in range(1, count + 1):
            section_slug, section_title = SECTIONS[(index - 1) % len(SECTIONS)]
            topic_count = 1 + ((index - 1) % len(topics))
            topic_start = (index - 1) % len(topics)
            selected_topics = [topics[(topic_start + offset) % len(topics)] for offset in range(topic_count)]
            primary_topic = selected_topics[0]
            title = f"{keyword} {section_title} {primary_topic.name} Result {index:02d}"
            if index == count:
                title += " With A Deliberately Long Search Result Heading"

            description = (
                f"{keyword} local QA result for {section_title} filtered by {primary_topic.name}. "
                "This description is intentionally predictable."
            )
            page = GeneralPage(
                title=title,
                slug=f"{keyword_slug}-{section_slug}-result-{index:02d}",
                locale=locale,
                theme="default",
                show_hero=False,
                seo_title=title,
                search_description=description,
                author=author,
            )
            section_roots[section_slug].add_child(instance=page)
            page.topics.add(*selected_topics)
            page.save_revision().publish()

            published_at = now - timedelta(days=count - index)
            page.first_published_at = published_at
            page.last_published_at = published_at
            page.save(update_fields=["first_published_at", "last_published_at"])
            section_counts[section_slug] += 1

        self.stdout.write(self.style.SUCCESS(f"Created and published {count} search test pages."))
        self.stdout.write(self.style.SUCCESS(f"Search for: {keyword}"))
        self.stdout.write(f"Expected pages at 10 results per page: {(count + 9) // 10}")
        for section_slug, section_title in SECTIONS:
            self.stdout.write(f"{section_title}: {section_counts[section_slug]}")

        if options["update_index"]:
            self.stdout.write("Running update_index...")
            call_command("update_index")
            self.stdout.write(self.style.SUCCESS("update_index complete."))
