from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST' and 'image' in request.FILES:  # Ensure the 'image' key is in request.FILES
        myimage = request.FILES['image']  # Access the uploaded image from request.FILES
        # Create an instance of Gallery and save the image  # Save the object to the database
        # return redirect('index')  # Redirect back to the index page after saving
        todo123=request.POST.get("todo")
        todo321=request.POST.get("date")
        todo311=request.POST.get("course")  
        obj=Gallery(title1=todo123,title2=todo321,title3=todo311,feedimage=myimage,user=request.user)
        obj.save()
        data=Gallery.objects.all()
        return redirect(sellerfirstpage)
    # Retrieve all gallery images to display
    gallery_images = Gallery.objects.all()
    return render(request, "index.html")

def sellersignup(request):
    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

        # Validate form fields
        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('sellerlogin')  # Redirect to login page

    return render(request, "register.html")

def sellerlogin(request):
    if 'username' in request.session:
        return redirect('index')  
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            if user.is_staff:
                return redirect('sellerfirstpage')
            return redirect('firstpage')  # Redirect to the home page
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'sellerlogin.html')

# def verifyotp(request):
#     if request.POST:
#         otp = request.POST.get('otp')
#         otp1 = request.session.get('otp')
#         if otp == otp1:
#             del request.session['otp']
#             return redirect('passwordreset')
#         else:
#             messages.error(request, 'Invalid OTP. Please try again.')

#     # Generate OTP and send email
#     otp = ''.join(random.choices('123456789', k=6))
#     request.session['otp'] = otp
#     message = f'Your email verification code is: {otp}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [request.session.get('email')]
#     send_mail('Email Verification', message, email_from, recipient_list)

#     return render(request, "otp.html")




def verifyotp(request):
    if request.POST:
        otp = request.POST.get('otp')
        otp1 = request.session.get('otp')
        otp_time_str = request.session.get('otp_time')  # This is now a string, not a datetime object

        # Check if OTP is expired
        if otp_time_str:
            otp_time = datetime.fromisoformat(otp_time_str)  # Convert the string back to a datetime object
            otp_expiry_time = otp_time + timedelta(minutes=5)  # OTP expires after 5 minutes
            if datetime.now() > otp_expiry_time:
                messages.error(request, 'OTP has expired. Please request a new one.')
                del request.session['otp']
                del request.session['otp_time']
                return redirect('verifyotp')  # Redirect to request a new OTP

        if otp == otp1:
            del request.session['otp']
            del request.session['otp_time']
            return redirect('passwordreset')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    # Generate OTP and send email
    otp = ''.join(random.choices('123456789', k=6))
    request.session['otp'] = otp
    request.session['otp_time'] = datetime.now().isoformat()  # Store the current time as an ISO string
    message = f'Your email verification code is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.session.get('email')]
    send_mail('Email Verification', message, email_from, recipient_list)

    return render(request, "otp.html")





def getusername(request):
    if request.POST:
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['email'] = user.email
            return redirect('verifyotp')
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return redirect('getusername')

    return render(request, 'getusername.html')

def passwordreset(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

        # Check if the passwords match
        if confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        else:
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)

                # Set the new password
                user.set_password(password)
                user.save()

                # After resetting password, clear the session email
                del request.session['email']
                messages.success(request, "Your password has been reset successfully.")
                
                # Optionally, log the user in automatically after resetting the password
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)

                return redirect('sellerlogin')  # Redirect to the login page after password reset
            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
                return redirect('getusername')  # Redirect to username input form

    return render(request, "passwordreset.html")

def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect(sellerlogin)
def firstpage(request):
    # Default value for `data`
    
    # if request.method == 'POST':
    #     # Handle POST logic
    #     todo123 = request.POST.get("todo")
    #     todo321 = request.POST.get("date")
    #     todo311 = request.POST.get("course")
        
    #     obj = Gallery(title1=todo123, title2=todo321, title3=todo311)
    #     obj.save()
    #     return redirect('firstpage')  # Redirect after saving the data

    # Handle GET request
    gallery_images = Gallery.objects.all()
    return render(request, "firstpage.html", {"gallery_images": gallery_images})
def usersignup(request):
    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

        # Validate form fields
        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('userlogin')  # Redirect to login page

    return render(request, "userregister.html")
def userlogin(request):
    if 'username' in request.session:
        return redirect('firstpage')  
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('firstpage')  # Redirect to the home page
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'userlogin.html')
def sellerfirstpage(request):
    data = Gallery.objects.all()
    gallery_images = Gallery.objects.filter(user=request.user)
    return render(request,'sellerfirstpage.html',{"gallery_images": gallery_images})
def delete_g(request,id):
    feeds=Gallery.objects.filter(pk=id)
    feeds.delete()
    return redirect(index)
def add(request):
    return render(request,"index.html")

@login_required
def edit_g(request, id):
    # Fetch the Gallery object or return a 404 if not found
    gallery_image = get_object_or_404(Gallery, pk=id, user=request.user)
    
    if request.method == 'POST':
        # Fetch form fields and image
        todo123 = request.POST.get("todo")
        todo321 = request.POST.get("date")
        todo311 = request.POST.get("course")
        myimage = request.FILES.get('image')  # Use `.get` to avoid KeyError
        
        # Validate form fields (example: ensure none are empty)
        if not todo123 or not todo321 or not todo311:
            messages.error(request, "All fields are required.")
            return render(request, 'index.html', {'data1': gallery_image})
        
        # Update the object
        gallery_image.title1 = todo123
        gallery_image.title2 = todo321
        gallery_image.title3 = todo311
        if myimage:  # Only update the image if one is provided
            gallery_image.feedimage = myimage
        gallery_image.save()

        messages.success(request, "Gallery item updated successfully!")
        return redirect('sellerfirstpage')

    # Handle GET request to display the form
    return render(request, 'index.html', {'data1': gallery_image})
def review(request):
    return render(request,"review.html")
def aboutus(request):
    return render(request,"aboutus.html")
def product(request,id):
    # data = Gallery.objects.all()
    gallery_images =Gallery.objects.filter(pk=id)
    return render(request,'products.html',{"gallery_images": gallery_images})
def add_to_cart(request, id):
    data1=id
    gallery_images =Gallery.objects.filter(pk=id)
    gallery_images = Gallery.objects.all()
    return render(request,'add_to_cart.html',{"gallery_images": gallery_images})
    

    