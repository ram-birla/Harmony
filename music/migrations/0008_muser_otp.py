# Generated by Django 2.2.3 on 2020-03-15 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20200228_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='muser',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]
