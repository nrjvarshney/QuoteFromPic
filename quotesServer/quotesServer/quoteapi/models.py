from django.db import models

class Image(models.Model):
    base64string = models.CharField(max_length=3276800, null=False)


    def __str__(self):
        return self.base64string