# Generated by Django 5.0.2 on 2024-07-22 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextExtractor', '0002_alter_fileupload_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]