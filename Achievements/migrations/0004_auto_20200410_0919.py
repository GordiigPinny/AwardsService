# Generated by Django 3.0.4 on 2020-04-10 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Achievements', '0003_auto_20200407_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievement',
            name='pic_link',
        ),
        migrations.AddField(
            model_name='achievement',
            name='pic_id',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
