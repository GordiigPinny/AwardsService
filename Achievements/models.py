from django.db import models
from Achievements.managers import AchievementManager


class Achievement(models.Model):
    """
    Модель ачивки
    """
    name = models.CharField(max_length=128, null=False, blank=False)
    descr = models.CharField(max_length=512, null=False, blank=True, default='')
    pic_link = models.URLField(null=False, blank=True, default='')
    created_dt = models.DateTimeField(auto_now_add=True)
    deleted_flg = models.BooleanField(default=False)

    objects = AchievementManager()

    def soft_delete(self):
        self.deleted_flg = True
        self.save(update_fields=['deleted_flg'])

    def __str__(self):
        return f'Achievement {self.name}'
