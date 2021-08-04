from django.db import models
from django.urls import reverse


class List(models.Model):
    
    def get_absolute_url(self):
        return reverse('page_list', args=[self.id])


class Item(models.Model):
    class Meta:
        unique_together = ('list', 'text',)
        ordering = ('id',)

    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
