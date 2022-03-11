# Generated by Django 3.2.12 on 2022-03-11 20:35

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0009_researchauthorrelation_researchdetailpageresearchregionrelation_researchregion_researchtopic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchDetailPageResearchTopicRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('research_detail_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_topics', to='wagtailpages.researchdetailpage')),
                ('research_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_research', to='wagtailpages.researchtopic')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
