from django.db import models
from Pins.managers import PinManager


class Pin(models.Model):
    """
    Модель пина (штуки на карте)
    """
    PLACE_PIN, USER_PIN = 'p', 'u'
    PIN_TYPE_CHOICES = (
        (PLACE_PIN, 'Место'),
        (USER_PIN, 'Юзер'),
    )

    objects = PinManager()

    name = models.CharField(max_length=128, null=False, blank=False)
    descr = models.CharField(max_length=1024, null=False, blank=True, default='')
    ptype = models.CharField(choices=PIN_TYPE_CHOICES, max_length=2, null=False)
    price = models.IntegerField(null=False, blank=False)
    pic_id = models.PositiveIntegerField(null=False, default=1)
    created_dt = models.DateTimeField(auto_now_add=True)
    deleted_flg = models.BooleanField(default=False, null=False)

    def soft_delete(self):
        self.deleted_flg = True
        self.save(update_fields=['deleted_flg'])

    def __str__(self):
        return f'{self.ptype}pin {self.name}'
