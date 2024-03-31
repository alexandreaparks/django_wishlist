from django.db import models

# Create your models here.


# create a Place model
class Place(models.Model):
    # relates to a table in database called Place with 2 columns and their attributes - name and visited
    # migrate to create the Place table
    # Django also creates a primary key(id) column - default is an auto-incrementing integer
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):  # user won't see this - helpful for developing
        return f'{self.name} visited? {self.visited}'
