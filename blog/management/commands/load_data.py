from django.core.management.base import BaseCommand
from blog.models import User, Post, Comment, Like, Favorite, Follow
from mimesis import Person
from faker import Faker
import random

class Command(BaseCommand):
    help = "Create fake data for testing blog layout"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print('Deleting database!')
        Post.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Comment.objects.all().delete()
        Favorite.objects.all().delete()
        Like.objects.all().delete()

        person = Person()
        fake = Faker()
        # populator = Faker.getPopulator()

        users = []
        for fake_user in range(100):
            fake_user = User.objects.create_user(person.username(), person.email(), 'password')
            users.append(fake_user)
        print("100 Fake users created!")

        fake_posts = []
        for i in range(50):
            post_dictionary = {
                'title': fake.sentence(),
                'description': fake.text(),
                'user': users[random.randrange(100)],
            }
            fake_posts.append(post_dictionary)

        posts = []
        for post_data in fake_posts:
            post = Post.objects.create(**post_data)
            posts.append(post)
        print('50 Posts imported!!!')

        for i in range(100):
            Like.objects.create(post=posts[random.randrange(50)], user=users[i])
        print('100 Likes imported!!!')

        for i in range(100):
            Favorite.objects.create(post=posts[random.randrange(50)], user=users[i])
        print('100 Favorites imported!!!')

        for i in range(200):
            Comment.objects.create(post=posts[random.randrange(50)], user=users[random.randrange(100)], comment=fake.sentence())
        print('200 comments imported!')

        for i in range(100):
            Follow.objects.create(following=users[i], followed=users[random.randrange(30)])
        print('100 follows imported!')

        print('All data imported successfully!')
