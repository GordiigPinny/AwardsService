from django.db.models import Manager


class PinManager(Manager):
    """
    ORM менеджер для Pin
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted_flg=False)

    def with_deleted(self):
        return super().get_queryset()
