from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from django.views.generic import View
from django.http import HttpResponse, request
from django.shortcuts import render
from django.contrib import messages
from .forms import FileUploadForm
from .models import FileUpload
import pytesseract
import threading
import datetime
import shutil
import time
import cv2
import os



destination_path = r"D:\\newDir\\"
class OnMyWatch(View):
    watchDirectory = r"D:\\datatowatch\\"
    def __init__(self, watchDirectory):
        self.watchDirectory = watchDirectory
        self.observer = Observer()

    def on_my_watch_view(self):
        try:
            event_handler = Handler()
            self.observer.schedule(event_handler, self.watchDirectory)
            self.observer.start()
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer Stopped")
        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self):
        self.destination_path = destination_path
    def on_created(self, event):
        if not event.is_directory:
            print("Watchdog received created event - %s." % event.src_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")        
            imagePath = event.src_path
            cordPath = event.src_path
            imagePath = imagePath.replace(".txt",".jpg")
            cordPath = cordPath.replace(".jpg",".txt")
            movepath = os.path.join(destination_path, timestamp)
            if (os.path.exists(imagePath) & os.path.exists(cordPath)):
                if (os.path.exists(movepath) == False):
                    os.makedirs(movepath)
                    time.sleep(5)
                    shutil.move(imagePath, movepath + "\\input.jpg")
                    shutil.move(cordPath, movepath + "\\input.txt")
                    extractor.extract_image(movepath + "\\input.jpg", movepath + "\\input.txt", movepath)
                 
    # def on_modified(self, event):
    #     if not event.is_directory:
    #         print("Watchdog received modified event - %s." % event.src_path)
    #         timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            
    #         imagePath = event.src_path;
    #         cordPath = event.src_path;
    #         imagePath = imagePath.replace(".txt",".jpg");
    #         cordPath = cordPath.replace(".jpg",".txt");
    #         if  (os.path.exists(imagePath) & os.path.exists(cordPath)):
    #             if (os.path.exists(os.path.join(destination_path,timestamp)) == False):
    #                 os.makedirs(os.path.join(destination_path, timestamp))
    
    
class ImageExtractor:
    def extractdata(self, text, sourcetext):
        name = ""
        fname = ""
        gname = ""
        cname = ""
        dname = ""
        lines = text.split("\n")
        for line in lines:
            if ":" in line:
                array = line.split(":")
                if ("name" in array[0].lower() and "father" not in array[0].lower()):
                    name = array[1].strip()
                elif ("father" in array[0].lower()):
                    fname = array[1].strip()
                elif ("gender" in array[0].lower()):
                    gname = array[1].strip()
                elif ("class" in array[0].lower()):
                    cname = array[1].strip()
                elif ("/" in array[1].lower()):
                    dname = array[1].strip()
                    
        with open("Final_Ouput.txt", "a") as finalwriter:
            finalwriter.write( os.path.split(sourcetext)[0] + "," +  os.path.split(sourcetext)[1] +","+  name + "," + fname + "," + gname + "," + cname + "," + dname + "\n")
            
            
    def extract_image(self, image, coordinates, output_path):
        index = 0
        with open(coordinates, "r") as f:
            for line in f.readlines():
                a = line.replace(" ","").replace("\n","").replace("\r","")
                # print(a)
                arr = a.split(",")
                index += 1
                # print(arr)
                coord_arr = []
                if len(arr) == 4:
                    arr = list(map(int, arr))
                    # print(arr)
                    img = cv2.imread(image)
                    if img is not None:  # Check if the image is not empty
                        left, upper, right, lower = arr[0], arr[1], arr[2], arr[3]
                        cropped_img = img[upper:lower, left:right]
                        output_file = os.path.join(output_path, f'{index}.jpg')
                        output_file_txt = os.path.join(output_path, f'{index}.txt')
                        cv2.imwrite(output_file, cropped_img)
                        img = cv2.imread(output_file)
                        text = pytesseract.image_to_string(img)
                        
                        with open(output_file_txt, "w") as textwriter:
                            textwriter.write(text)
                        extractor.extractdata(text, output_file_txt)
                    else:
                        print("Error: Enter Valid Coordinates.")
                        


def file_upload_view(request):
    class_obj = OnMyWatch(watchDirectory="D:\\datatowatch\\")
    thread = threading.Thread(target=class_obj.on_my_watch_view)
    thread.daemon = True
    thread.start()
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

def success_view(request):
    return HttpResponse('Files uploaded successfully!')
    
extractor = ImageExtractor()

if __name__ == '__main__':
    watch = OnMyWatch(watchDirectory="D:\\datatowatch\\")
    watch.run()
    