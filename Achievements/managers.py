from django.db.models import Manager


class AchievementManager(Manager):
    """
    ORM менеджер для ачивок
    """
    def get_queryset(self):
        return super().get_queryset().filter(deleted_flg=False)

    def with_deleted(self):
        return super().get_queryset()
