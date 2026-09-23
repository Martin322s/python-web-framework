from django.db.models import Count

from django.db import models

class CustomDirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(movies_count=Count('director_movies')).order_by('-movies_count', 'full_name')