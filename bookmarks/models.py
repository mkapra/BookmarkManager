from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.tag_name


class Bookmark(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=500)
    link = models.CharField(max_length=255, blank=False)
    tags = models.ManyToManyField(Tag)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.link}"
