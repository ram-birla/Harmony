# Generated by Django 2.2.3 on 2020-02-28 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_muser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='fcount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='song',
            name='clickCount',
            field=models.IntegerField(default=0),
        ),
    ]
