# Generated by Django 5.0.2 on 2024-07-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextExtractor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='D:\\datatowatch'),
        ),
    ]
