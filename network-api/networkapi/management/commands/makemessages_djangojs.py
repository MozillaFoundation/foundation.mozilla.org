from django.core.management.commands.makemessages import Command as MMCommand


class Command(MMCommand):
    """
    Wrapper for the makemessages command to force makemessages call xgettext
    with the language provided as input.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            '-lang',
            default='Python',
            dest='language',
            help='Language to be used by xgettext'
        )

        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        language = options.get('language')
        self.xgettext_options.append('--language={lang}'.format(
            lang=language
        ))

        super(Command, self).handle(*args, **options)
