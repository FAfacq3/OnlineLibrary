from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import UserProfile, Material, Review
from django.core.files.base import ContentFile
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with test users, materials, and reviews'

    def handle(self, *args, **kwargs):
        self.create_users_and_profiles()
        self.create_materials()
        self.create_reviews()
        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))

    def create_users_and_profiles(self):
        for i in range(5):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='password123')
                profile = UserProfile.objects.create(
                    user=user,
                    bio=fake.sentence(),
                    birth_date=fake.date_of_birth(minimum_age=18, maximum_age=40)
                )
                print(f'Created user {username}')

    def create_materials(self):
        users = User.objects.all()
        categories = ['Book', 'Video', 'Audio', 'Software', 'Image']

        for i in range(10):
            user = random.choice(users)
            material = Material.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=150),
                category=random.choice(categories),
                uploaded_by=user
            )
            material.file.save(f'testfile_{i}.txt', ContentFile('Sample content for testing.'))
            material.save()
            print(f'Created material: {material.title} by {user.username}')

    def create_reviews(self):
        users = User.objects.all()
        materials = Material.objects.all()

        for i in range(10):
            material = random.choice(materials)
            user = random.choice(users)
            Review.objects.create(
                material=material,
                user=user,
                rating=random.randint(1, 5),
                comment=fake.sentence(),
            )
            print(f'Added review by {user.username} to {material.title}')
