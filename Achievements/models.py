from django.db import models


class Achievement(models.Model):
    """
    Модель ачивки
    """
    name = models.CharField(max_length=128, null=False, blank=False)
    descr = models.CharField(max_length=512, null=True, blank=True)
    pic_link = models.URLField(null=True, blank=True)
    deleted_flg = models.BooleanField(default=False)

    def __str__(self):
        return f'Achievement {self.name}'
