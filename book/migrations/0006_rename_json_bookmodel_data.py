# Generated by Django 3.2.8 on 2021-10-14 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_alter_bookmodel_json'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmodel',
            old_name='json',
            new_name='data',
        ),
    ]
