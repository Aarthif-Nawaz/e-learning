# Generated by Django 3.2.5 on 2021-07-16 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0014_rename_user_registration'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Registration',
            new_name='User',
        ),
    ]
