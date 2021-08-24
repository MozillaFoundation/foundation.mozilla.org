# Generated by Django 3.1.11 on 2021-08-18 02:31

from django.db import migrations
import networkapi.wagtailpages.pagemodels.blog.blog_category
import wagtail.core.blocks
import wagtail.core.blocks.static_block
import wagtail.core.fields
import wagtail.images.blocks

from networkapi.mozfest.models import MozfestPrimaryPage


def loop_through_pages_with_image_blocks(apps, schema):

    for page in MozfestPrimaryPage.objects.all():
        if hasattr(page, 'alias_of') and page.alias_of != None:
            # This is a page alias, rather than a real page
            continue
        # If this page doesn't have a Image that needs update, don't save it.
        # This will speed up how fast this task can run
        needs_saving = False
        # Only loop through streamfield data if there's a `body` field on the page
        if page.body:
            # Checking if page.body has raw_data, and looping through it.
            if hasattr(page.body, 'raw_data'):
                for block in page.body.raw_data:
                    # If the block type is an image,
                    # check if the image has the wide setting on.
                    if 'type' in block and block['type'] == "image":
                        # If so, set the new image_width value to wide.
                        if 'wide_image' in block['value'] and block['value']['wide_image'] == True:
                            block['value']['image_width'] = "wide"
                            needs_saving = True

            # If page is published already, continue to publish it.
            # Otherwise just save a revision for draft history.
            if needs_saving:
                revision = page.save_revision()
                if page.live:
                    revision.publish()

class Migration(migrations.Migration):

    dependencies = [
        ('mozfest', '0016_auto_20210525_1516'),
    ]

    operations = [
        # Adding the new "image_width" field.
        migrations.AlterField(
            model_name='mozfestprimarypage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'large', 'h2', 'h3', 'h4', 'h5', 'ol', 'ul', 'link', 'hr'])), ('card_grid', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alt_text', wagtail.core.blocks.CharBlock(help_text="Alt text for card's image.", required=False)), ('title', wagtail.core.blocks.CharBlock(help_text='Heading for the card.')), ('body', wagtail.core.blocks.TextBlock(help_text='Body text of the card.')), ('link_url', wagtail.core.blocks.CharBlock(help_text='URL that this card should link out to.')), ('link_label', wagtail.core.blocks.CharBlock(help_text='Label for the URL link above.'))]), help_text='Please use a minimum of 2 cards.'))])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('altText', wagtail.core.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('captionURL', wagtail.core.blocks.CharBlock(help_text='Optional URL that this caption should link out to.', required=False)), ('wide_image', wagtail.core.blocks.BooleanBlock(default=False, help_text='Would you like to use a wider image on desktop?', required=False)), ('image_width', wagtail.core.blocks.ChoiceBlock(choices=[('normal', 'Normal'), ('wide', 'Wide'), ('full_width', 'Full Width')], help_text='Wide images are col-12, Full-Width Images reach both ends of the screen (16:6 images recommended for full width)'))])), ('image_text', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('altText', wagtail.core.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'link'])), ('url', wagtail.core.blocks.CharBlock(help_text='Optional URL that this image should link out to.', required=False)), ('top_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider above content block.', required=False)), ('bottom_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider below content block.', required=False))])), ('image_text_mini', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('altText', wagtail.core.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link']))])), ('image_grid', wagtail.core.blocks.StructBlock([('grid_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Alt text for this image.', required=False)), ('caption', wagtail.core.blocks.CharBlock(help_text='Please remember to properly attribute any images we use.', required=False)), ('url', wagtail.core.blocks.CharBlock(help_text='Optional URL that this figure should link out to.', required=False)), ('square_image', wagtail.core.blocks.BooleanBlock(default=True, help_text='If left checked, the image will be cropped to be square.', required=False))])))])), ('video', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.CharBlock(help_text='For YouTube: go to your YouTube video and click “Share,” then “Embed,” and then copy and paste the provided URL only. For example: https://www.youtube.com/embed/3FIVXBawyQw For Vimeo: follow similar steps to grab the embed URL. For example: https://player.vimeo.com/video/9004979')), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('captionURL', wagtail.core.blocks.CharBlock(help_text='Optional URL for caption to link to.', required=False)), ('video_width', wagtail.core.blocks.ChoiceBlock(choices=[('normal', 'Normal'), ('wide', 'Wide'), ('full_width', 'Full Width')], help_text='Wide videos are col-12, Full-Width videos reach both ends of the screen.'))])), ('iframe', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.CharBlock(help_text='Please note that only URLs from white-listed domains will work.')), ('height', wagtail.core.blocks.IntegerBlock(help_text='Optional integer pixel value for custom iFrame height', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('captionURL', wagtail.core.blocks.CharBlock(help_text='Optional URL that this caption should link out to.', required=False)), ('iframe_width', wagtail.core.blocks.ChoiceBlock(choices=[('normal', 'Normal'), ('wide', 'Wide'), ('full_width', 'Full Width')], help_text='Wide iframes are col-12, Full-Width iframes reach both ends of the screen'))])), ('linkbutton', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock()), ('URL', wagtail.core.blocks.CharBlock()), ('styling', wagtail.core.blocks.ChoiceBlock(choices=[('btn-primary', 'Primary button'), ('btn-secondary', 'Secondary button')]))])), ('spacer', wagtail.core.blocks.StructBlock([('size', wagtail.core.blocks.ChoiceBlock(choices=[('1', 'quarter spacing'), ('2', 'half spacing'), ('3', 'single spacing'), ('4', 'one and a half spacing'), ('5', 'triple spacing')]))])), ('quote', wagtail.core.blocks.StructBlock([('quotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.CharBlock()), ('attribution', wagtail.core.blocks.CharBlock(required=False))])))])), ('pulse_listing', wagtail.core.blocks.StructBlock([('search_terms', wagtail.core.blocks.CharBlock(help_text='Test your search at mozillapulse.org/search', label='Search', required=False)), ('max_number_of_results', wagtail.core.blocks.IntegerBlock(default=6, help_text='Choose 1-12. If you want visitors to see more, link to a search or tag on Pulse.', max_value=12, min_value=0, required=True)), ('only_featured_entries', wagtail.core.blocks.BooleanBlock(default=False, help_text='Featured items are selected by Pulse moderators.', label='Display only featured entries', required=False)), ('newest_first', wagtail.core.blocks.ChoiceBlock(choices=[('True', 'Show newer entries first'), ('False', 'Show older entries first')], label='Sort')), ('advanced_filter_header', wagtail.core.blocks.static_block.StaticBlock(admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------', label=' ')), ('issues', wagtail.core.blocks.ChoiceBlock(choices=[('all', 'All'), ('Decentralization', 'Decentralization'), ('Digital Inclusion', 'Digital Inclusion'), ('Online Privacy & Security', 'Online Privacy & Security'), ('Open Innovation', 'Open Innovation'), ('Web Literacy', 'Web Literacy')])), ('help', wagtail.core.blocks.ChoiceBlock(choices=[('all', 'All'), ('Attend', 'Attend'), ('Create content', 'Create content'), ('Code', 'Code'), ('Design', 'Design'), ('Fundraise', 'Fundraise'), ('Join community', 'Join community'), ('Localize & translate', 'Localize & translate'), ('Mentor', 'Mentor'), ('Plan & organize', 'Plan & organize'), ('Promote', 'Promote'), ('Take action', 'Take action'), ('Test & feedback', 'Test & feedback'), ('Write documentation', 'Write documentation')], label='Type of help needed')), ('direct_link', wagtail.core.blocks.BooleanBlock(default=False, help_text='Checked: user goes to project link. Unchecked: user goes to pulse entry', label='Direct link', required=False))])), ('profile_listing', wagtail.core.blocks.StructBlock([('max_number_of_results', wagtail.core.blocks.IntegerBlock(default=12, help_text='Pick up to 48 profiles.', max_value=48, min_value=1, required=True)), ('advanced_filter_header', wagtail.core.blocks.static_block.StaticBlock(admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------', label=' ')), ('profile_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Fellow.', required=False)), ('program_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Tech Policy.', required=False)), ('year', wagtail.core.blocks.CharBlock(default='', required=False))])), ('profile_by_id', wagtail.core.blocks.StructBlock([('ids', wagtail.core.blocks.CharBlock(help_text='Show profiles for pulse users with specific profile ids (mozillapulse.org/profile/[##]). For multiple profiles, specify a comma separated list (e.g. 85,105,332).', label='Profile by ID'))])), ('profile_directory', wagtail.core.blocks.StructBlock([('max_number_of_results', wagtail.core.blocks.IntegerBlock(default=12, help_text='Pick up to 48 profiles.', max_value=48, min_value=1, required=True)), ('advanced_filter_header', wagtail.core.blocks.static_block.StaticBlock(admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------', label=' ')), ('profile_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Fellow.', required=False)), ('program_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Tech Policy.', required=False)), ('year', wagtail.core.blocks.CharBlock(default='', required=False)), ('filter_values', wagtail.core.blocks.CharBlock(default='2019,2018,2017,2016,2015,2014,2013', help_text='Example: 2019,2018,2017,2016,2015,2014,2013', required=True))])), ('recent_blog_entries', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('tag_filter', wagtail.core.blocks.CharBlock(help_text='Test this filter at foundation.mozilla.org/blog/tags/', label='Filter by Tag', required=False)), ('category_filter', wagtail.core.blocks.ChoiceBlock(choices=networkapi.wagtailpages.pagemodels.blog.blog_category.BlogPageCategory.get_categories, help_text='Test this filter at foundation.mozilla.org/blog/category/', label='Filter by Category', required=False)), ('top_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider above content block.', required=False)), ('bottom_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider below content block.', required=False))])), ('blog_set', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('top_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider above content block.', required=False)), ('bottom_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider below content block.', required=False)), ('blog_pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(page_type=['wagtailpages.BlogPage'])))])), ('airtable', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text="Copied from the Airtable embed code. The word 'embed' will be in the url")), ('height', wagtail.core.blocks.IntegerBlock(default=533, help_text='The pixel height on desktop view, usually copied from the Airtable embed code'))])), ('typeform', wagtail.core.blocks.StructBlock([('embed_id', wagtail.core.blocks.CharBlock(help_text='The embed id of your Typeform page (e.g. if the form is on admin.typeform.com/form/e8zScc6t, the id will be: e8zScc6t)', required=True)), ('button_type', wagtail.core.blocks.ChoiceBlock(choices=[('btn-primary', 'Primary button'), ('btn-secondary', 'Secondary button')])), ('button_text', wagtail.core.blocks.CharBlock(help_text='This is a text prompt for users to open the typeform content', required=True))]))]),
        ),        
        # Updating "image_width" of any image with "wide" set to True.
        migrations.RunPython(loop_through_pages_with_image_blocks),
        # Removing old "Wide" boolean field
        migrations.AlterField(
            model_name='mozfestprimarypage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'large', 'h2', 'h3', 'h4', 'h5', 'ol', 'ul', 'link', 'hr'])), ('card_grid', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alt_text', wagtail.core.blocks.CharBlock(help_text="Alt text for card's image.", required=False)), ('title', wagtail.core.blocks.CharBlock(help_text='Heading for the card.')), ('body', wagtail.core.blocks.TextBlock(help_text='Body text of the card.')), ('link_url', wagtail.core.blocks.CharBlock(help_text='URL that this card should link out to.')), ('link_label', wagtail.core.blocks.CharBlock(help_text='Label for the URL link above.'))]), help_text='Please use a minimum of 2 cards.'))])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('altText', wagtail.core.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('captionURL', wagtail.core.blocks.CharBlock(help_text='Optional URL that this caption should link out to.', required=False)), ('image_width', wagtail.core.blocks.ChoiceBlock(choices=[('normal', 'Normal'), ('wide', 'Wide'), ('full_width', 'Full Width')], help_text='Wide images are col-12, Full-Width Images reach both ends of the screen (16:6 images recommended for full width)'))])), ('image_text', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('altText', wagtail.core.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'link'])), ('url', wagtail.core.blocks.CharBlock(help_text='Optional URL that this image should link out to.', required=False)), ('top_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider above content block.', required=False)), ('bottom_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider below content block.', required=False))])), ('image_text_mini', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('altText', wagtail.core.blocks.CharBlock(help_text='Image description (for screen readers).', required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link']))])), ('image_grid', wagtail.core.blocks.StructBlock([('grid_items', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Alt text for this image.', required=False)), ('caption', wagtail.core.blocks.CharBlock(help_text='Please remember to properly attribute any images we use.', required=False)), ('url', wagtail.core.blocks.CharBlock(help_text='Optional URL that this figure should link out to.', required=False)), ('square_image', wagtail.core.blocks.BooleanBlock(default=True, help_text='If left checked, the image will be cropped to be square.', required=False))])))])), ('video', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.CharBlock(help_text='For YouTube: go to your YouTube video and click “Share,” then “Embed,” and then copy and paste the provided URL only. For example: https://www.youtube.com/embed/3FIVXBawyQw For Vimeo: follow similar steps to grab the embed URL. For example: https://player.vimeo.com/video/9004979')), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('captionURL', wagtail.core.blocks.CharBlock(help_text='Optional URL for caption to link to.', required=False)), ('video_width', wagtail.core.blocks.ChoiceBlock(choices=[('normal', 'Normal'), ('wide', 'Wide'), ('full_width', 'Full Width')], help_text='Wide videos are col-12, Full-Width videos reach both ends of the screen.'))])), ('iframe', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.CharBlock(help_text='Please note that only URLs from white-listed domains will work.')), ('height', wagtail.core.blocks.IntegerBlock(help_text='Optional integer pixel value for custom iFrame height', required=False)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('captionURL', wagtail.core.blocks.CharBlock(help_text='Optional URL that this caption should link out to.', required=False)), ('iframe_width', wagtail.core.blocks.ChoiceBlock(choices=[('normal', 'Normal'), ('wide', 'Wide'), ('full_width', 'Full Width')], help_text='Wide iframes are col-12, Full-Width iframes reach both ends of the screen'))])), ('linkbutton', wagtail.core.blocks.StructBlock([('label', wagtail.core.blocks.CharBlock()), ('URL', wagtail.core.blocks.CharBlock()), ('styling', wagtail.core.blocks.ChoiceBlock(choices=[('btn-primary', 'Primary button'), ('btn-secondary', 'Secondary button')]))])), ('spacer', wagtail.core.blocks.StructBlock([('size', wagtail.core.blocks.ChoiceBlock(choices=[('1', 'quarter spacing'), ('2', 'half spacing'), ('3', 'single spacing'), ('4', 'one and a half spacing'), ('5', 'triple spacing')]))])), ('quote', wagtail.core.blocks.StructBlock([('quotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.CharBlock()), ('attribution', wagtail.core.blocks.CharBlock(required=False))])))])), ('pulse_listing', wagtail.core.blocks.StructBlock([('search_terms', wagtail.core.blocks.CharBlock(help_text='Test your search at mozillapulse.org/search', label='Search', required=False)), ('max_number_of_results', wagtail.core.blocks.IntegerBlock(default=6, help_text='Choose 1-12. If you want visitors to see more, link to a search or tag on Pulse.', max_value=12, min_value=0, required=True)), ('only_featured_entries', wagtail.core.blocks.BooleanBlock(default=False, help_text='Featured items are selected by Pulse moderators.', label='Display only featured entries', required=False)), ('newest_first', wagtail.core.blocks.ChoiceBlock(choices=[('True', 'Show newer entries first'), ('False', 'Show older entries first')], label='Sort')), ('advanced_filter_header', wagtail.core.blocks.static_block.StaticBlock(admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------', label=' ')), ('issues', wagtail.core.blocks.ChoiceBlock(choices=[('all', 'All'), ('Decentralization', 'Decentralization'), ('Digital Inclusion', 'Digital Inclusion'), ('Online Privacy & Security', 'Online Privacy & Security'), ('Open Innovation', 'Open Innovation'), ('Web Literacy', 'Web Literacy')])), ('help', wagtail.core.blocks.ChoiceBlock(choices=[('all', 'All'), ('Attend', 'Attend'), ('Create content', 'Create content'), ('Code', 'Code'), ('Design', 'Design'), ('Fundraise', 'Fundraise'), ('Join community', 'Join community'), ('Localize & translate', 'Localize & translate'), ('Mentor', 'Mentor'), ('Plan & organize', 'Plan & organize'), ('Promote', 'Promote'), ('Take action', 'Take action'), ('Test & feedback', 'Test & feedback'), ('Write documentation', 'Write documentation')], label='Type of help needed')), ('direct_link', wagtail.core.blocks.BooleanBlock(default=False, help_text='Checked: user goes to project link. Unchecked: user goes to pulse entry', label='Direct link', required=False))])), ('profile_listing', wagtail.core.blocks.StructBlock([('max_number_of_results', wagtail.core.blocks.IntegerBlock(default=12, help_text='Pick up to 48 profiles.', max_value=48, min_value=1, required=True)), ('advanced_filter_header', wagtail.core.blocks.static_block.StaticBlock(admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------', label=' ')), ('profile_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Fellow.', required=False)), ('program_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Tech Policy.', required=False)), ('year', wagtail.core.blocks.CharBlock(default='', required=False))])), ('profile_by_id', wagtail.core.blocks.StructBlock([('ids', wagtail.core.blocks.CharBlock(help_text='Show profiles for pulse users with specific profile ids (mozillapulse.org/profile/[##]). For multiple profiles, specify a comma separated list (e.g. 85,105,332).', label='Profile by ID'))])), ('profile_directory', wagtail.core.blocks.StructBlock([('max_number_of_results', wagtail.core.blocks.IntegerBlock(default=12, help_text='Pick up to 48 profiles.', max_value=48, min_value=1, required=True)), ('advanced_filter_header', wagtail.core.blocks.static_block.StaticBlock(admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------', label=' ')), ('profile_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Fellow.', required=False)), ('program_type', wagtail.core.blocks.CharBlock(default='', help_text='Example: Tech Policy.', required=False)), ('year', wagtail.core.blocks.CharBlock(default='', required=False)), ('filter_values', wagtail.core.blocks.CharBlock(default='2019,2018,2017,2016,2015,2014,2013', help_text='Example: 2019,2018,2017,2016,2015,2014,2013', required=True))])), ('recent_blog_entries', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('tag_filter', wagtail.core.blocks.CharBlock(help_text='Test this filter at foundation.mozilla.org/blog/tags/', label='Filter by Tag', required=False)), ('category_filter', wagtail.core.blocks.ChoiceBlock(choices=networkapi.wagtailpages.pagemodels.blog.blog_category.BlogPageCategory.get_categories, help_text='Test this filter at foundation.mozilla.org/blog/category/', label='Filter by Category', required=False)), ('top_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider above content block.', required=False)), ('bottom_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider below content block.', required=False))])), ('blog_set', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('top_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider above content block.', required=False)), ('bottom_divider', wagtail.core.blocks.BooleanBlock(help_text='Optional divider below content block.', required=False)), ('blog_pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(page_type=['wagtailpages.BlogPage'])))])), ('airtable', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text="Copied from the Airtable embed code. The word 'embed' will be in the url")), ('height', wagtail.core.blocks.IntegerBlock(default=533, help_text='The pixel height on desktop view, usually copied from the Airtable embed code'))])), ('typeform', wagtail.core.blocks.StructBlock([('embed_id', wagtail.core.blocks.CharBlock(help_text='The embed id of your Typeform page (e.g. if the form is on admin.typeform.com/form/e8zScc6t, the id will be: e8zScc6t)', required=True)), ('button_type', wagtail.core.blocks.ChoiceBlock(choices=[('btn-primary', 'Primary button'), ('btn-secondary', 'Secondary button')])), ('button_text', wagtail.core.blocks.CharBlock(help_text='This is a text prompt for users to open the typeform content', required=True))]))]),
            ),    
    ]
