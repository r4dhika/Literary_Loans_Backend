from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.module_loading import autodiscover_modules
from django.core.management import call_command

def populate_data(sender, **kwargs):
    # Call the management commands to populate default data and create superuser
    call_command('populate_genre')

class LiteraryloansAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'literaryLoans_app'

    def ready(self):
        # Connect the signal to the populate_data function
        autodiscover_modules('management')
        post_migrate.connect(populate_data, sender=self)
