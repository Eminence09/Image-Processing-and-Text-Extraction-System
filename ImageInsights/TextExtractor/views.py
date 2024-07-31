from watchdog.events import FileSystemEventHandler
from TextExtractor.forms import FileUploadForm
from TextExtractor.models import FileUpload
from watchdog.observers import Observer
from django.views.generic import View
from django.shortcuts import render
from django.contrib import messages
from PIL import Image
import base64
import os
import io


def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image_file']
            coordinates_file = request.FILES['coordinates_file']
            # file_upload = FileUpload(image_file=image_file, coordinates_file=coordinates_file)
            file_upload=FileUpload.objects.create(image_file=image_file, coordinates_file=coordinates_file)
            print(file_upload)
            file_upload.save()
            messages.success(request, 'Form submission successful')
    else:
        form = FileUploadForm()
    return render(request, 'file_upload.html', {'form': form})



def read_file(request):
    f = open("D:\\User_DataBase\\Final_Output.txt", 'r')
    file_contents = f.readlines()    
    arraydata = []
    lineNumber = 1
    for line in file_contents:
            array = line.split(",")
            array.append(lineNumber)
            lineNumber = lineNumber + 1
            arraydata.append(array[2:])
    f.close()
    # print(arraydata)
    context = {'file_contents': arraydata}
    return render(request, "display_data.html", context)



def each_line(request, line_no):
    f = open("D:\\User_DataBase\\Final_Output.txt", 'r')
    file_data = f.readlines()
    f.close()
    if line_no <= len(file_data) and line_no > 0:
        line = file_data[line_no-1]
        arr = line.split(",")
        filepath = os.path.join(arr[0], arr[1].replace(".txt", ".jpg"))
        print(filepath) 
        with open(filepath, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())   
            decoded = my_string.decode('ascii')
        myString = "data:image/jpg;base64," + decoded + ""
        return render(request, "myimage.html", {'pathstr': myString})
    else:
        return render(request, "text.html", {'Line': "No line"})