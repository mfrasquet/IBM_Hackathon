# Generated by Django 2.0.5 on 2018-11-20 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0002_auto_20181120_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='contract',
            name='title',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
