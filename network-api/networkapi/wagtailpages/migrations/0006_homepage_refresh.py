from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


def create_authors(apps, schema_editor):
    """
    Convert text-based authors to snippet authors and assigns each author
    to the BlogPage
    """
    BlogPage = apps.get_model('wagtailpages', 'BlogPage')
    BlogAuthor = apps.get_model('wagtailpages', 'BlogAuthor')
    BlogAuthors = apps.get_model('wagtailpages', 'BlogAuthors')

    for post in BlogPage.objects.all():
        author, _ = BlogAuthor.objects.get_or_create(name=post.author)
        BlogAuthors.objects.create(page=post, author=author)


def remove_authors(apps, schema_editor):
    """
    Convert snippets to author text fields.

    Because this is an Oderable, we'll use the first author for the CharField.
    """
    BlogPage = apps.get_model('wagtailpages', 'BlogPage')

    for post in BlogPage.objects.all():
        author = post.authors.first()
        if author.author:
            post.author = author.author.name
            post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailpages', '0005_auto_20200811_1657'),
    ]

    operations = [
       migrations.RemoveField(
            model_name='blogpage',
            name='author_fy_NL',
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_de',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_en',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_es',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_fr',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_fy_NL',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cause_statement_link', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_de',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_en',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_es',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_fr',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_fy_NL',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_nl',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_pl',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_link_text_pt',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_nl',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_pl',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='cause_statement_pt',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_background_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_heading',
            field=models.CharField(default='Partner with us', max_length=75),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_intro_text',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parnter_internal_link', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='partner_page_text',
            field=models.CharField(default="Let's work together", max_length=35),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_de',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_en',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_es',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_fr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_fy_NL',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_nl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_pl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_image_pt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_image', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_de',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_en',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_es',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_fr',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_fy_NL',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_nl',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_pl',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_job_title_pt',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_de',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_en',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_es',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_fr',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_fy_NL',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_nl',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_pl',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_source_name_pt',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text',
            field=models.CharField(default='', max_length=450),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_de',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_en',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_es',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_fr',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_fy_NL',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_nl',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_pl',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='quote_text_pt',
            field=models.CharField(default='', max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='spotlight_headline',
            field=models.CharField(blank=True, help_text='Spotlight headline', max_length=140),
        ),
        migrations.AddField(
            model_name='homepage',
            name='spotlight_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spotlight_image', to='wagtailimages.Image'),
        ),
        migrations.CreateModel(
            name='PartnerLogos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link', models.URLField(blank=True)),
                ('logo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_logos', to='wagtailpages.Homepage')),
            ],
            options={
                'verbose_name': 'Partner Logo',
            },
        ),
        migrations.CreateModel(
            name='HomepageSpotlightPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailpages.BlogPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='spotlight_posts', to='wagtailpages.Homepage')),
            ],
            options={
                'verbose_name': 'blog',
                'verbose_name_plural': 'blogs',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='HomepageNewsYouCanUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailpages.BlogPage')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_you_can_use', to='wagtailpages.Homepage')),
            ],
            options={
                'verbose_name': 'blog',
                'verbose_name_plural': 'blogs',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='FocusArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of this area of focus. Max. 100 characters.', max_length=100)),
                ('description', models.TextField(help_text='Description of this area of focus. Max. 300 characters.', max_length=300)),
                ('external_link', models.URLField(blank=True)),
                ('interest_icon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interest_icon', to='wagtailimages.Image')),
                ('internal_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internal_link', to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Area of focus',
                'verbose_name_plural': 'Areas of focus',
            },
        ),
        migrations.CreateModel(
            name='AreaOfFocus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailpages.FocusArea')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas_of_focus', to='wagtailpages.Homepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image')),
            ],
        ),
        migrations.CreateModel(
            name='BlogAuthors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailpages.BlogAuthor')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='wagtailpages.BlogPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RunPython(create_authors, reverse_code=remove_authors),
        migrations.RemoveField(
            model_name='blogpage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_de',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_en',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_es',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_fr',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_nl',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_pl',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='author_pt',
        ),
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
