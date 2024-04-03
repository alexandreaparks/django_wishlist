from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# create a Place model
class Place(models.Model):
    # relates to a table in database called Place with columns and their attributes
    # migrate to create the Place table
    # Django also creates a primary key(id) column - default is an auto-incrementing integer

    # user is a foreign key to Django's built-in User model
    # if user is deleted, their places are deleted too
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):  # user won't see this - helpful for developing
        # string method will use the url of the image if a photo exists for a place
        # if no photo exists for a place, the string will say 'no photo'
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'  # truncate to first 100 characters in notes fields
        return (f'{self.pk}: {self.name} visited? {self.visited} on {self.date_visited}'
                f'\nNotes: {notes_str}'
                f'\nPhoto URL: {photo_str}')
