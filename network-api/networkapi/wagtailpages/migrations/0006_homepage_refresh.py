# Generated by Django 2.2.14 on 2020-08-19 20:14

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailpages', '0005_ia_refresh_updates'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageFocusAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomepageTakeActionCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('text', models.CharField(max_length=255)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image')),
                ('internal_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Take Action Card',
                'ordering': ['sort_order'],
            },
        ),
        migrations.AlterModelOptions(
            name='partnerlogos',
            options={'ordering': ['sort_order'], 'verbose_name': 'Partner Logo'},
        ),
        migrations.RemoveField(
            model_name='focusarea',
            name='external_link',
        ),
        migrations.RemoveField(
            model_name='focusarea',
            name='internal_link',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_de',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_es',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_fr',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_fy_NL',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_nl',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_pl',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='hero_story_description_pt',
        ),
        migrations.AddField(
            model_name='focusarea',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='take_action_title',
            field=models.CharField(default='Take action', max_length=50),
        ),
        migrations.AddField(
            model_name='partnerlogos',
            name='name',
            field=models.CharField(default='Partner Name', help_text='Alt text for the logo image.', max_length=100),
        ),
        migrations.AddField(
            model_name='partnerlogos',
            name='width',
            field=models.PositiveSmallIntegerField(default=100, help_text='The width of the image. Height will automatically be applied.'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_de',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_en',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_es',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_fr',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_fy_NL',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_nl',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_pl',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='hero_headline_pt',
            field=models.CharField(blank=True, help_text='Hero story headline', max_length=80, null=True),
        ),
        migrations.DeleteModel(
            name='AreaOfFocus',
        ),
        migrations.AddField(
            model_name='homepagetakeactioncards',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='take_action_cards', to='wagtailpages.Homepage'),
        ),
        migrations.AddField(
            model_name='homepagefocusareas',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailpages.FocusArea'),
        ),
        migrations.AddField(
            model_name='homepagefocusareas',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='focus_areas', to='wagtailpages.Homepage'),
        ),
        migrations.RemoveField(
            model_name='homepagefeaturedhighlights',
            name='highlight',
        ),
        migrations.RemoveField(
            model_name='homepagefeaturedhighlights',
            name='page',
        ),
        migrations.DeleteModel(
            name='HomepageFeaturedBlogs',
        ),
        migrations.DeleteModel(
            name='HomepageFeaturedHighlights',
        ),
    ]
