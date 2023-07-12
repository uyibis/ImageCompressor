"""
Definition of views.
"""

from contextlib import redirect_stdout
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import  RegisterForm
from django.shortcuts import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseBadRequest
import io
import math



def home(request):
    """Renders the home page."""
    if request.method == 'GET':
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year':datetime.now().year,
            }
        )
    if request.method == 'POST' and request.FILES['myfile']:
        #if request.method == 'POST' and request.FILES.get('myfile'):
        # Get the uploaded file from the request
        uploaded_file = request.FILES['myfile']
        
        # Check if the uploaded file is an image
        if not uploaded_file.content_type.startswith('image/'):
            return HttpResponseBadRequest('Invalid file type')
        
        try:
            # Open the uploaded image using PIL
            image = Image.open(uploaded_file)
            
            # Compress the image
            compressed_image = io.BytesIO()
            image.save(compressed_image, format='JPEG', optimize=True)
            compressed_image.seek(0)
            
            # Create a new InMemoryUploadedFile with the compressed image
            compressed_file = InMemoryUploadedFile(
                compressed_image,
                None,
                uploaded_file.name,
                uploaded_file.content_type,
                None,
                None
            )
            
            # Save the compressed image to a temporary file
            saved_file = default_storage.save('temp.jpg', ContentFile(compressed_file.read()))
            
            # Get the URL of the compressed image
            image_url = default_storage.url(saved_file)
            return render(request, 'app/index.html', {
            'uploaded_file_url': image_url
            })
            
            #return HttpResponse(f'Image compressed successfully. Here is the link: {image_url}')
        
        except IOError:
            return HttpResponseBadRequest(IOError)#'Error occurred while compressing the image')
    
    return HttpResponseBadRequest('No file uploaded or invalid request method')
        

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def welcome(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/home.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'app/register.html', { 'form': form}) 
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        print(form);
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print("data save")
            #messages.success(request, 'You have singed up successfully.')
            #login(request, user)
            return HttpResponse('done')
        else:
            print("form is invalid")
            return render(request, 'app/register.html', {'form': form})
