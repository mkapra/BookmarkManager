# Generated by Django 3.1.4 on 2020-12-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_auto_20201210_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
