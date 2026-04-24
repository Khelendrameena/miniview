from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.db import models
from app.models import Profile
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.cache import cache
import xml.etree.ElementTree as ET
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime
from collections import defaultdict
from difflib import get_close_matches
import uuid
import requests
import json
import os
import random
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # ya 'home_page'

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # login URL name
    return render(request, 'index.html')

def custom_500_error(request):
    return render(request, '500.html', status=500)
    
def google_login(request):
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&scope=email profile"
    )
    return redirect(google_auth_url)

def google_callback(request):
    code = request.GET.get('code')

    # Exchange code for access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=token_data).json()

    # Get user info
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_response = requests.get(
        user_info_url,
        headers={"Authorization": f"Bearer {token_response['access_token']}"},
    ).json()

    # Authenticate user in Django
    email = user_info_response['email']
    name = user_info_response.get('name', 'Google User')

    # Check if the user exists
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0],
            'first_name': name,
        }
    )

    # If user is newly created, make the password unusable
    if created:
        user.set_unusable_password()
        user.save()

        # Store additional info in the session
        request.session['name'] = name
        request.session['emailp'] = email
        return render(request, 'username_edit.html')  # Redirect to username edit page

    # If user exists, log them in directly
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Specify backend
    return redirect('/')

def usernameedit(request):
    if request.session.get('emailp') is not None:
        username = request.POST.get('username')
        email = request.session.get('emailp')
        name = request.session.get('name')

        if email and username:
            id_4 = uuid.uuid1()
            profile = Profile(
                profile_id=id_4,
                profile_picture=f'https://ui-avatars.com/api/?name={name}',
                name=name,
                username=username,
                followers=0,
                following=0,
                country="in"
            )
            profile.save()

            user_obj = User.objects.get(email=email)
            user_obj.username = username
            user_obj.save()

            login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')  # Specify backend
            return redirect('/')
        else:
            return HttpResponse("Something went wrong")
    else:
        return HttpResponse("User not authenticated")

# Signup View
def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error': "Passwords do not match."})
        elif User.objects.filter(email=email).exists():
            return redirect('login')

        otp_generated = random.randint(100000, 999999)

        # Temporarily store user details in the session
        request.session['name'] = name
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = otp_generated

        # Send OTP via email
        subject = "Welcome to NewsWatch"
        message = f"Thank you for signing up to NewsWatch!<br>Your OTP is <h1>{otp_generated}</h1>"
        from_email = "khelendra1112@gmail.com"
        send_mail(subject, message, from_email, [email])

        return redirect('otp')  # Redirect to OTP view after signup
    return render(request, 'signup.html')


# OTP Verification View
def otp_view(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if otp and int(otp) == session_otp:
            # Create user after OTP verification
            name = request.session.get('name')
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')
            id_4 = uuid.uuid1()
            request.session['id_4'] = id_4
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            profile = Profile(profile_id=id_4,profile_picture=f'https://ui-avatars.com/api/?name={name}',name=name,username=username,followers=0,following=0,country="in")
            profile.save()
            # Clear session data
            request.session.flush()

            return redirect('/login')  # Redirect to login after successful signup
        else:
            return render(request, 'otp.html', {'error': "Invalid OTP."})

    return render(request, 'otp.html')


#Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the given email exists
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Replace '/' with your desired redirect page
            else:
                return render(request, 'login.html', {'error': "Invalid email or password."})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': ""})

    return render(request, 'login.html')

def profile(request, username):
    if Profile.objects.filter(username=username).exists():
        data = Profile.objects.filter(username=username).first()  # Get a single profile
        id = Profile.objects.filter(username=username).first().profile_id
        request.session['profile_id'] = id
        model_data = MyModel.objects.all()
        # Convert the response to JSON
        json_data = content_data(request,f'@{username}',[])
        json_data["data"] = data
        
        if request.user.username is not None:
           try:
                profile = Profile.objects.get(username=request.user.username)
                json_data["name"] = profile.name
                json_data["image_url"] = profile.profile_picture
           except Profile.DoesNotExist:
                json_data["name"] = 'none'
                json_data["image_url"] = 'none'
        else:
            json_data["name"] = 'none'
            json_data["image_url"] = 'none'
        
        if UserReaction.objects.filter(username=request.user.username,follow_to=username).exists():
            json_data["follow_status"] = UserReaction.objects.filter(username=request.user.username,follow_to=username).first().follow
        else:
            json_data["follow_status"] = -1
        for arti in json_data["articles"]:
           if "s" not in arti:
              arti["date"] = arti["publishedAt"]
              arti["name"]:Profile.objects.get(username='justwatch').name
              arti["profile_url"]: "justwatch"
              arti["profile_pic"]: Profile.objects.filter(username='justwatch').first().profile_picture

           if UserReaction.objects.filter(vlog_id=arti["publishedAt"]).exists():
              arti["like_status"] = UserReaction.objects.get(vlog_id=arti["publishedAt"]).like
           else:
              arti["like_status"] = 0
           
           if UserReaction.objects.filter(username=request.user.username,follow_to=arti["profile_pic"].replace("@",'')).exists():
               arti["follow_status"] = UserReaction.objects.filter(username=request.user.username,follow_to=arti["profile_pic"].replace("@",'')).first().follow
           else:
               arti["follow_status"] = -1
           matching_model = model_data.filter(id=arti["publishedAt"])
           if matching_model.exists():
               # If it exists, safely fetch the 'views' and 'likes'
               arti["views"] = matching_model.values('views')[0]['views']
               arti["likes"] = matching_model.values('likes')[0]['likes']
           else:
               arti["views"] = 0
               arti["likes"] = 0
           if comentconfig.objects.all().exists():
               # If it exists, safely fetch the 'views' and 'likes'
               data = comentconfig.objects.all().filter(mainid=arti["publishedAt"])
               serialized_data = serialize('json', data)
               coment_data = json.loads(serialized_data)
               arti["coment"] = len(coment_data)
           else:
               arti["coment"] = 0
               
        json_data["path"] = f'/@{username}/'
        json_data["time"] = datetime.now().year
        if request.method == 'POST':
        # अगर सेशन में index उपलब्ध नहीं है तो इसे प्रारंभ करें
           if 'index' not in request.session:
               request.session['index'] = 5

        # अगले 5 व्लॉग्स लाएं
           start = request.session['index']
           end = start + 5
           if start >= len(json_data["articles"]):
               return JsonResponse({'html': '', 'message': 'No more articles'})
           json_data_2 = json_data["articles"][start:end]
           request.session['index'] = end  # सेशन में index को अपडेट करें
           json_data["articles"] = json_data_2
           html = render_to_string('vlog_html_2.html', json_data, request=request)
           return JsonResponse({'html': html})
        else:
            # पहला पेज लोड करने के लिए index को रीसेट करें
            request.session['index'] = 5
            json_data_4 = json_data["articles"][:5]
            json_data["articles"] = json_data_4
            return render(request, 'profile.html', json_data)
    else:
        return redirect('/signup')



def profilebin(request,username):
    if request.user.username is not None:
        if username == request.user.username:
           return render(request, 'edit.html')
        else:
           return HttpResponse("something wrong")
    else:
        return redirect('login')

def vlog(request, username):
    if username == request.user.username:
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            vlog_id = generate_unique_datetime_string()
            thumbnail = None

            if 'thumbnail' in request.FILES:
                uploaded_file = request.FILES['thumbnail']
                static_path = os.path.join(settings.BASE_DIR, 'media') 

                if not os.path.exists(static_path):
                    os.makedirs(static_path)

                file_name = f"thumbnail_{vlog_id}.jpg"  # Ensure it has a valid image extension
                check_and_delete(file_name, '/media')
                file_path = os.path.join(static_path, file_name)

                # Save the uploaded file temporarily
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Resize the image to 200x200
                try:
                    with Image.open(file_path) as img:
                        img = img.convert("RGB")  # Ensure the image is in RGB format
                        img = img.resize((720,400), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
                        img.save(file_path, "JPEG")  # Save as JPEG format
                except IOError:
                    return HttpResponse("Uploaded file is not a valid image.")

                thumbnail = f"/media/{file_name}"
            
            # Save data in the database
            DraftVlog.objects.create(
                user=request.user,
                vlog_id=vlog_id,
                thumbnail=thumbnail,
                title=title,
                description=description,
            )

            return render(request, 'vlog_des.html')
        else:
            return render(request, 'vlog.html')
    else:
        return HttpResponse("Something went wrong")




def follow(request,username_2):
    if request.method == "POST":
       if request.user.username is not None and request.user.username != '':
          data = json.loads(request.body)
          id = data.get('id')
          follow = data.get('follow')
          user_reaction, created = UserReaction.objects.update_or_create(
             vlog_id=id,
             defaults={
                "follow": follow,
                "username": request.user.username,
                "follow_to": username_2,
              },
              )
          profile = Profile.objects.get(profile_id=id)
          profile_2 = Profile.objects.get(username=request.user.username)
          profile.followers = profile.followers + follow
          profile_2.following = profile_2.following + follow
          if username_2 != request.user.username:
              profile.save()
              profile_2.save()
              return HttpResponse("done")
          else:
              return HttpResponse("something wrong")
       else:
            return redirect('/login')
    else:
        return HttpResponse("something wrong")

def profiledit(request):
    profile_id = request.session.get('profile_id')# Retrieve the profile ID from the POST request
    try:
        profile = Profile.objects.get(profile_id=profile_id)  # Fetch the profile object

        # Update profile fields
        profile.name = request.POST.get('name')

        # Handle file upload
        if 'pic' in request.FILES:
            uploaded_file = request.FILES['pic']
            static_path = os.path.join(settings.BASE_DIR, 'media')  # Path to static/uploads

            # Create the directory if it doesn't exist
            if not os.path.exists(static_path):
                os.makedirs(static_path)

            # Generate a unique filename to prevent overwriting
            file_name = f"profile_{profile_id}"
            check_and_delete(file_name,'/media')
            file_path = os.path.join(static_path, file_name)

            # Save the file
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Generate the URL for the uploaded file
            file_url = f"/media/{file_name}"

            # Update profile picture URL
            profile.profile_picture = file_url

        # Update other profile fields
        profile.des = request.POST.get('Bio')
        profile.save()
        username = profile.username
        # Return the file link in the response
        return redirect(f'/@{username}')

    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist
        return HttpResponse("Profile not found", status=404)

    except Exception as e:
        # Handle other exceptions
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
