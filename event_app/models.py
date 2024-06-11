from django.db import models
from course_app.models import Mode,Language,Location,Collaborators,Producers,Authors,Sponsors,Topics

# Create your models here.

class Speakers(models.Model):
    speaker_name=models.CharField(max_length=20)
    speaker_img=models.ImageField(upload_to='speakers_img')


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time=models.TimeField()
    event_price = models.IntegerField()
    event_learning_credits = models.IntegerField(default=None)
    event_lifetime_learners = models.IntegerField(default=None)
    event_rating= models.FloatField(max_length=20)
    event_first_published=models.DateField()
    event_num_ratings = models.IntegerField()
    event_times_launched = models.IntegerField()
    event_num_interested = models.IntegerField()
    event_num_hours = models.IntegerField()
    event_num_days = models.IntegerField()
    # event_topic=models.CharField(max_length=255)
    event_skills=models.CharField(max_length=200)
    more_about_event=models.TextField()
    event_relevance_of_program=models.TextField()
    event_recommended_learners=models.TextField()
    event_what_will_learn=models.TextField()
    event_img=models.ImageField(upload_to='event_pics')

    # foreign keys
    event_medium_of_communication = models.ForeignKey(Language, on_delete=models.CASCADE)
    event_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    event_mode = models.ForeignKey(Mode, on_delete=models.CASCADE, default=None)
    event_authors = models.ManyToManyField(Authors, related_name='events',default=None)
    event_collab = models.ManyToManyField(Collaborators, related_name='events', default=None)
    event_producers = models.ManyToManyField(Producers,related_name='events',default=None)
    event_sponsors=models.ManyToManyField(Sponsors,related_name='events',default=None)
    event_topic=models.ManyToManyField(Topics,related_name='events',default=None)

