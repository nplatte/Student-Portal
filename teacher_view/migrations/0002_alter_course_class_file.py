# Generated by Django 4.2.6 on 2023-11-08 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_view', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='Class_File',
            field=models.FileField(blank=True, null=True, upload_to='class_htmls'),
        ),
    ]
