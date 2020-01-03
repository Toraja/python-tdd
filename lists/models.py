from django.db import models


class Item(models.Model):
    """Docstring for Item. """

    text = models.TextField(default='')
