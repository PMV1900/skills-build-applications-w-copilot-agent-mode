from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

# Define models inline for demonstration; in a real app, these would be in models.py
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    points = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            user_objs.append(user)

        # Create activities
        Activity.objects.create(user='ironman', activity_type='Running', duration=30, team='Marvel')
        Activity.objects.create(user='spiderman', activity_type='Cycling', duration=45, team='Marvel')
        Activity.objects.create(user='batman', activity_type='Swimming', duration=60, team='DC')
        Activity.objects.create(user='superman', activity_type='Yoga', duration=20, team='DC')

        # Create leaderboard
        Leaderboard.objects.create(user='ironman', points=100, team='Marvel')
        Leaderboard.objects.create(user='spiderman', points=80, team='Marvel')
        Leaderboard.objects.create(user='batman', points=90, team='DC')
        Leaderboard.objects.create(user='superman', points=110, team='DC')

        # Create workouts
        Workout.objects.create(name='HIIT', description='High Intensity Interval Training', difficulty='Hard')
        Workout.objects.create(name='Cardio', description='Cardio workout', difficulty='Medium')
        Workout.objects.create(name='Strength', description='Strength training', difficulty='Hard')
        Workout.objects.create(name='Stretch', description='Stretching routine', difficulty='Easy')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
