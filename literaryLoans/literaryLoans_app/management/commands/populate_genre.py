from django.core.management.base import BaseCommand
from literaryLoans_app.models import Genre

class Command(BaseCommand):
    help = 'Populate backend with default data'

    def handle(self, *args, **kwargs):
        # Check if default data exists, if not, create it
        if not Genre.objects.exists():
            # Create default data
            Genre.objects.create(
                title="Fiction", 
                description="Imaginative stories created by the author, often set in fictional worlds or based on real-life events."
            )
            Genre.objects.create(
                title="Non-Fiction", 
                description="Fact-based books that explore real events, people, or subjects, providing information or analysis."
            )
            Genre.objects.create(
                title="Mystery", 
                description="Stories centered around solving a crime or unraveling a puzzle, often with suspenseful elements."
            )
            Genre.objects.create(
                title="Romance", 
                description="Books focusing on romantic relationships, love, and emotional connections between characters."
            )
            Genre.objects.create(
                title="Thriller", 
                description="Fast-paced narratives filled with suspense, tension, and excitement, often involving danger or high stakes."
            )
            Genre.objects.create(
                title="Fantasy", 
                description="Stories set in imaginary worlds with magic, mythical creatures, and epic adventures."
            )
            Genre.objects.create(
                title="Horror", 
                description="Books designed to evoke fear, often featuring supernatural elements, monsters, or psychological terror."
            )
            Genre.objects.create(
                title="Technology", 
                description=" Works focusing on scientific advancements, digital culture, and the impact of technology on society and individuals."
            )
            Genre.objects.create(
                title="History", 
                description="Books documenting past events, cultures, and societies, providing context and understanding of the past."
            )
            self.stdout.write(self.style.SUCCESS('Default data populated successfully'))
        else:
            self.stdout.write(self.style.WARNING('Default data already exists'))
