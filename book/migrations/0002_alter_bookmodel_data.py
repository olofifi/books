# Generated by Django 3.2.8 on 2021-10-14 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='data',
            field=models.JSONField(default=None),
        ),
    ]
