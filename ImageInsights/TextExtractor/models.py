# models.py
from django.db import models
from django.shortcuts import render
class FileUpload(models.Model):
    image_file = models.FileField(default='default_coordinates.txt')
    coordinates_file = models.FileField()