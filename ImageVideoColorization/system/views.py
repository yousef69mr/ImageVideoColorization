from django.shortcuts import render
from django.http import JsonResponse,FileResponse,HttpResponseBadRequest
import os 

from django.conf import settings
from django.core.files.storage import default_storage
from datetime import datetime
from PIL import Image
# Create your views here.


def colorizationModelView(request):

    if request.method == 'POST':
        colorized_image = request.POST.get('raw_file_input',None)
        print(colorized_image)
        return render(request,'colorization.html',{
            'colorized_image':colorized_image
        })
    return render(request,'colorization.html') 
    

def create_file(file):
    extenstion = os.path.splitext(file.name)
    print(extenstion)
    file_name = extenstion[0] + extenstion[1]
    print(file_name)

    now = datetime.now()
    y = now.strftime("%y")
    m = now.strftime("%m")
    d = now.strftime("%d")
    if extenstion[1] in ('.jpg', '.jpeg', '.png', '.gif'):
        file_type = 'images'
    elif extenstion[1] in ('.mp4', '.avi', '.mov', '.wmv'):
        file_type = "videos"
    else:
        file_type = 'files'
    file_directory= os.path.join(f'{file_type}'+'\\'+str(y)+'\\'+str(m)+'\\'+str(d)+'\\')
    file_url= os.path.join(f'media/{file_type}/'+str(y)+'/'+str(m)+'/'+str(d)+'/',file_name)

    print(file_directory)
    full_image_directory = os.path.join(settings.MEDIA_ROOT,file_directory)

    try:
        os.makedirs(full_image_directory, exist_ok = True)
        print("Directory '%s' created successfully" % file_directory)
    except OSError as error:
        print("Directory '%s' can not be created" % file_directory)

    file_path = os.path.join(full_image_directory,file_name)
    #print(image_path)
    print(os.getcwd())
    os.chdir(str(full_image_directory))
    print(os.getcwd())
    #targetFile = os.path.join(path, image)
    print(file_path)

    ###################################
    
    with open(default_storage.path(file_path),'wb+') as destination:
        print("write")
        for chunk in file.chunks() :
            destination.write(chunk)

    return file_url


def process_form_view(request):
    if request.method == 'POST':
        media_file = request.FILES.get('media_file')
        print(media_file)
        try:
            if media_file is None:
                raise ValueError('No File is uploaded')
            # process the form data and return a response
            file_extension = os.path.splitext(media_file.name)[1].lower()
            if file_extension in ('.jpg', '.jpeg', '.png', '.gif'):
                # process the image
                
                # process on image file media
                # save output image  then return the url path
                # process the colored image and return a response
                image_url = create_file(media_file)
                # return the processed image as a response
                return JsonResponse({'success': True,'file_type':'image','message':'image created successfully','file':image_url},status=200)
            elif file_extension in ('.mp4', '.avi', '.mov', '.wmv'):

                # process on video file media
                # save output video  then return the url path
                video_url = image_url = create_file(media_file)
                # return the video file
                return JsonResponse({'success': True,'file_type':'video','message':'video created successfully','file':video_url},status=200)
                
            else:
                return HttpResponseBadRequest('Invalid media file type.')
            
        
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
    else:
        # return an error response if the request method is not POST
        data = {'error': 'Invalid request method.'}
        return JsonResponse(data, status=400)