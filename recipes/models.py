from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.BooleanField(auto_now_add=True)
    updated_at = models.BooleanField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.IMageField(upload_to='recipes/covers/%y/%m/%d/')

