from django import forms
from.models import FileUpload

class FileUploadForm(forms.Form):
    image_file = forms.FileField()
    coordinates_file = forms.FileField()
    
    class Meta:
        model = FileUpload
        fields = ('file',)
        