# Generated by Django 2.2.2 on 2019-08-06 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Class', '0009_assignment_assignment_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='assignment_creator',
            new_name='instructor',
        ),
    ]
