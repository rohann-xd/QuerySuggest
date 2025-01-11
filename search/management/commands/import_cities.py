import os
from django.core.management.base import BaseCommand
from search.models import City  

class Command(BaseCommand):
    help = 'Import city names from filenames in the data folder and store them in the City model'

    def handle(self, *args, **kwargs):
        # Define the path to your data folder (update if the path is different)
        data_folder_path = os.path.join(os.getcwd(), 'data')  # Assuming 'data' is in the root directory

        # List all files in the data folder
        filenames = os.listdir(data_folder_path)

        # Iterate over the filenames and process only .txt files
        for filename in filenames:
            if filename.endswith('.txt'):
                # Remove the .txt extension from the filename to get the city name
                city_name = filename[:-4]

                # Check if the city already exists in the database, avoid duplicates
                if not City.objects.filter(name=city_name).exists():
                    # Save the city name to the database
                    City.objects.create(name=city_name)
                    self.stdout.write(self.style.SUCCESS(f'Successfully added city: {city_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'City {city_name} already exists, skipping...'))
