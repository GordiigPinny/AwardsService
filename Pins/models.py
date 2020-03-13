from django.db import models


class Pin(models.Model):
    """
    Модель пина (штуки на карте)
    """
    PLACE_PIN, USER_PIN = 'p', 'u'
    PIN_TYPE_CHOICES = (
        (PLACE_PIN, 'Место'),
        (USER_PIN, 'Юзер'),
    )

    name = models.CharField(max_length=128, null=False, blank=False)
    descr = models.CharField(max_length=1024, null=True, blank=True)
    ptype = models.CharField(choices=PIN_TYPE_CHOICES, max_length=2, null=False)
    price = models.IntegerField(null=False, blank=False)
    img_link = models.URLField(null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    deleted_flg = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'{self.ptype}pin {self.name}'
