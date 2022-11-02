# Generated by Django 3.2.13 on 2022-08-09 12:03

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailpages', '0046_buyersguidepage_hero_supporting_articles_heading'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyersGuidePageFeaturedArticleRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailpages.buyersguidearticlepage')),
                ('locale', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_article_relations', to='wagtailpages.buyersguidepage')),
            ],
            options={
                'abstract': False,
                'unique_together': {('translation_key', 'locale')},
            },
        ),
    ]
