from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from app.models import MyModel
from app.models import Profile
from app.models import Vlog
from app.models import UserReaction
from app.models import comentconfig
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
#import numpy as np
from django.conf import settings
from datetime import datetime
from collections import defaultdict
from difflib import get_close_matches
import uuid
import requests
import json
import os
import random
main_id = []

def content_data(user_2):
    if user_2 == 'all':
        vlogs = Vlog.objects.all()
        vlog_data = [{
            "title": vlog.title,
            "description": vlog.description,
            "url": f"vlog/show/{vlog.vlog_id}",
            "urlToImage": vlog.thumbnail,
            "publishedAt": vlog.vlog_id,
            "date": vlog.date_posted,
            "name":Profile.objects.get(username=vlog.user.replace('@','')).name,
            "profile_url": f"{vlog.user}",
            "profile_pic": Profile.objects.filter(username=vlog.user.replace('@','')).first().profile_picture,
            "s":1
        } for vlog in vlogs]
        json_data = {"articles": vlog_data}
        return json_data
    else:
        vlogs = Vlog.objects.filter(user=user_2)
        vlog_data = [{
            "title": vlog.title,
            "description": vlog.description,
            "url": f"vlog/show/{vlog.vlog_id}",
            "urlToImage": vlog.thumbnail,
            "vlog_url": f"vlog/{vlog.vlog_id}",
            "publishedAt": vlog.vlog_id,
            "date": vlog.date_posted,
            "name": Profile.objects.get(username=user_2.replace('@','')).name,
            "profile_url": f"{vlog.user}",
            "profile_pic": Profile.objects.get(username=user_2.replace('@','')).profile_picture,
            "s":1
        } for vlog in vlogs]
        json_data = {"articles": vlog_data}
        return json_data

def suggest_vlogs(vlog_titles, user_liked_vlogs):    
    # Vectorize the vlog titles using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    vlog_vectors = vectorizer.fit_transform(vlog_titles)
    
    # Vectorize the liked vlog titles
    liked_vectors = vectorizer.transform(user_liked_vlogs)
    
    # Calculate the average of the liked vlog vectors
    average_liked_vector = liked_vectors.mean(axis=0)
    
    # Calculate similarity between the average liked vector and all vlogs
    similarity_scores = cosine_similarity(average_liked_vector, vlog_vectors)
    
    return similarity_scores[0]

def sort_vlogs_by_engagement(request,vlogs, user_interests):
    if not isinstance(vlogs, list):
        raise ValueError("Input must be a list of dictionaries representing vlogs.")
    
    if not isinstance(user_interests, list):
        raise ValueError("User interests must be a list of [interest, weight].")
    
    # Process user interests into a dictionary for easier lookup
    interest_weights = {interest.lower(): weight for interest, weight in user_interests}
    follow_boost = 50
    index = 0
    for vlog in vlogs:
        if not all(key in vlog for key in ["likes", "views","coment", "title"]):
            raise ValueError("Each vlog must have 'likes', 'comments', 'views', and 'title' keys.")
        current_date = datetime.now()        
        # Calculate engagement score
        vlog['engagement_score'] = (vlog['likes'] * 2) + (vlog['coment'] * 3) + (vlog['views'] * 1)
        if "s" in vlog:
           date_str = vlog["publishedAt"].split('-')[0][:8]
           posted_date = datetime.strptime(f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}",'%Y-%m-%d')
        else:        
           posted_date = posted_date = datetime.strptime(vlog["publishedAt"].split('T')[0], '%Y-%m-%d')
        days_since_posted = (current_date - posted_date).days
        time_decay_factor = max(0, 30 - days_since_posted)  # Decay reduces with days since posted
        vlog['time_decay_score'] = time_decay_factor  # Add time decay factor
        vlog['follow_boost'] = follow_boost if vlog['follow_status'] == 1 else 0
        # Calculate relevance score based on user interests
        if request.user.is_authenticated and 1 == 2:
        	vlog['relevance_score'] = suggest_vlogs([vlog["title"] for vlog in vlogs],[like_rect.title for like_rect in UserReaction.objects.filter(username=request.user1.username)])[index]*100
        	index = index + 1
        	vlog['combined_score'] = vlog['engagement_score'] + vlog['relevance_score'] + vlog['time_decay_score'] + vlog['follow_boost']
        else:
       	  vlog['combined_score'] = vlog['engagement_score'] + vlog['time_decay_score']
   
    # Sort vlogs by combined score in descending order
    sorted_vlogs = sorted(vlogs, key=lambda x: x['combined_score'], reverse=True)    
    return sorted_vlogs

search_2 = []
def home(request):
    labels = [
    "technology", "sports", "food", "travel", "health", "science", "politics", "entertainment", "music", 
    "movies", "education", "business", "art", "fashion", "finance", "history", "literature", "gaming", 
    "news", "lifestyle", "sports news", "tech news", "cooking", "recipes", "photography", "travel blog"]
    quary = labels[random.randint(0,len(labels)-1)]
    url = f"https://newsapi.org/v2/everything?q={quary}&apiKey=1388989202ef4521a5452bb1214daba7"
    response = requests.get(url)
    model_data = MyModel.objects.all()
    
    # Convert the response to JSON
    json_data = response.json()
    json_data["articles"] = [article for article in json_data["articles"] if article["title"] != "[Removed]"]
    json_data["articles"] = json_data["articles"]+content_data('all')["articles"]
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

    for arti in json_data["articles"]:
        # Check if any matching id is found
        if "s" not in arti:
            arti["date"] = arti["publishedAt"]
            arti["name"] = Profile.objects.get(username='justwatch').name
            arti["profile_url"] = "@justwatch"
            arti["profile_pic"] = Profile.objects.filter(username='justwatch').first().profile_picture
        search_2.append(arti["title"])
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
    user_interests = [
    ["travel", 0.9],
    ["sports", 0.7],
    ["technology", 0.8],
    ["food", 0.6]
    ]
    json_data["articles"] = sort_vlogs_by_engagement(request,json_data["articles"],user_interests)
    # Pass the data as context to the template
    json_data["articles"][-1]["end"] = 1
    json_data["path"] = '/'
    if request.method == 'POST':
        # अगर सेशन में index उपलब्ध नहीं है तो इसे प्रारंभ करें
        if 'index' not in request.session:
            request.session['index'] = 6

        # अगले 5 व्लॉग्स लाएं
        start = request.session['index']
        end = start + 5
        json_data_2 = json_data["articles"][start:end]
        request.session['index'] = end  # सेशन में index को अपडेट करें

        json_data["articles"] = json_data_2
        html = render_to_string('vlog_html.html', json_data, request=request)
        return JsonResponse({'html': html})
    else:
        # पहला पेज लोड करने के लिए index को रीसेट करें
        request.session['index'] = 6
        json_data_4 = json_data["articles"][:6]
        json_data["articles"] = json_data_4
        return render(request, 'index.html', json_data)


# Step 1: Build the Inverted Index
def build_inverted_index(vlogs):
    index = defaultdict(list)
    for i, vlog in enumerate(vlogs):
        # Create tokens from title and country
        for word in (vlog['title']).lower().split():
            index[word].append(i)
    return index

# Step 2: Find Closest Matches Using Fuzzy Matching
def fuzzy_search(query, index, vlogs, threshold=0.6):
    results = set()
    # Create a unique word list from the index
    all_words = list(index.keys())
    
    # Find closest matches for each query word
    for word in query.lower().split():
        # Get words that are similar to the query word
        matches = get_close_matches(word, all_words, n=5, cutoff=threshold)
        for match in matches:
            results.update(index[match])
    
    # Return the matched vlogs
    return [vlogs[i] for i in results]

quary_2 = []
def searchquary(request):
    if request.method == 'POST':
        quary = quary_2[-1]
    else:
        quary = request.GET.get('quary')
        quary_2.append(quary)
    url = f"https://newsapi.org/v2/everything?q={quary}&apiKey=1388989202ef4521a5452bb1214daba7"
    response = requests.get(url)
    model_data = MyModel.objects.all()

    # Convert the response to JSON
    json_data = response.json()
    json_data["articles"] = [article for article in json_data["articles"] if article["title"] != "[Removed]"]
    json_data["articles"] = json_data["articles"]+content_data('all')["articles"]
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

    for arti in json_data["articles"]:
        # Check if any matching id is found
        if "s" not in arti:
            arti["date"] = arti["publishedAt"]
            arti["name"] = Profile.objects.get(username='justwatch').name
            arti["profile_url"] = "@justwatch"
            arti["profile_pic"] = Profile.objects.filter(username='justwatch').first().profile_picture

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
    # Pass the data as context to the template
    user_interests = [
    ["travel", 0.9],
    ["sports", 0.7],
    ["technology", 0.8],
    ["food", 0.6]
    ]
    inverted_index = build_inverted_index(json_data["articles"])
    json_data["articles"] = fuzzy_search(quary,inverted_index,json_data["articles"])
    json_data["articles"][-1]["end"] = 1
    json_data["path"] = '/search/quary'
    if request.method == 'POST':
        # अगर सेशन में index उपलब्ध नहीं है तो इसे प्रारंभ करें
        if 'index' not in request.session:
            request.session['index'] = 6

        # अगले 5 व्लॉग्स लाएं
        start = request.session['index']
        end = start + 5
        json_data_2 = json_data["articles"][start:end]
        request.session['index'] = end  # सेशन में index को अपडेट करें

        json_data["articles"] = json_data_2
        html = render_to_string('vlog_html.html', json_data, request=request)
        return JsonResponse({'html': html})
    else:
        # पहला पेज लोड करने के लिए index को रीसेट करें
        request.session['index'] = 6
        json_data_4 = json_data["articles"][:6]
        json_data["articles"] = json_data_4
        return render(request, 'index.html', json_data)

def view(request):
    data = json.loads(request.body)
    id = data.get('id')
    status = data.get('status')
    views_reaction = status[0]
    like_reaction = status[1]
    if MyModel.objects.all().filter(id=id).exists():
         status[0] = status[0] + MyModel.objects.all().filter(id=id).first().views
         status[1] = status[1] + MyModel.objects.all().filter(id=id).first().likes
    user_reaction, created = UserReaction.objects.update_or_create(
        vlog_id=id,
        defaults={
            "views": views_reaction,
            "like": like_reaction,
            "username": request.user.username,
        }
    )
    model = MyModel(id=id,views=status[0],likes=status[1])
    model.save()
    return HttpResponse("something wrong")

def coment(request):
    if request.method == 'POST':
        id = request.POST.get("mainid")
        main_id.append(id)
        data = comentconfig.objects.filter(mainid=id)
        # Serialize the queryset to JSON
        serialized_data = serialize('json', data)
        print(main_id[len(main_id)-1],id)
        # Pass the serialized data to the template
        return render(request, 'coment.html', {'data': serialized_data})
    else:
        return HttpResponse("this is wrong")
        
def comentadd(request):
    if request.method == 'POST':
        try:
            mainid = main_id[-1]  # Get the last element from main_id
            data = json.loads(request.body)
            name = data.get('name')
            mess = data.get('mess')
            like = data.get('like')
            id = uuid.uuid1()

            # Save the comment to the database
            #user_reaction = UserReaction(vlog_id=main_id[-1],coment=1,username=request.user.username)
            coment = comentconfig(mainid=mainid, id=id, name=name, mess=mess, like=like)
            coment.save()
            #user_reaction.save()

            # Return a success response
            return JsonResponse({"status": "success", "message": "Comment added successfully."})
        except Exception as e:
            # Handle errors gracefully and return an appropriate response
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

def comentlikeadd(request):
      data = json.loads(request.body)
      id = data.get('id')
      like = data.get('like')
      if request.method == 'POST':
         if comentconfig.objects.all().filter(id=id).exists():
             coment = comentconfig.objects.get(id = id)
             coment.like = like
             coment.save()
             return HttpResponse("done")
         return HttpResponse("done")

def search(request):
   return render(request, 'search.html', {"search":search_2}) 


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
    if not User.objects.filter(email=email).exists():
	    # Check if user exists, else create a new user
	    user, _ = User.objects.get_or_create(username=email.split('@')[0], defaults={'first_name': name})
	    user.backend = 'django.contrib.auth.backends.ModelBackend'
	    request.session['name'] = name
	    request.session['emailp'] = email
	    return render(request, 'username_edit.html')	    
    else:
	    user_obj = User.objects.get(email=email)
	    user = authenticate(username=user_obj.username, password=password)
	    login(request, user)
	    return redirect('/')
	    
	    
	
def usernameedit(request):
	if request.user.username is not None:
	    if request.session['emailp'] is not None:
	    	username = request.POST.get('username')
	    	email = request.session['emailp']
	    	name = request.session['name']
	    	id_4 = uuid.uuid1()
	    	profile = Profile(profile_id=id_4
	    	,profile_picture=f'https://ui-avatars.com/api/?name={name}',name=name,username=username,followers=0,following=0,country="in")
	    	profile.save()
	    	user_obj = User.objects.get(email=email)
	    	user_obj.username = username
	    	user = authenticate(username=user_obj.username, password=password)
	    	login(request, user)
	    	return redirect('/')
	    else:
	    	  return  HttpResponse("something wrong")	    	  
	else:
	 	   return HttpResponse("something wrong")
	
	
	


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
                return render(request, 'login.html')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': "Invalid email or password."})

    return render(request, 'login.html')

id_profile = []
def profile(request, username):
    print(content_data(f'@{username}'))
    if Profile.objects.filter(username=username).exists():
        data = Profile.objects.filter(username=username).first()  # Get a single profile
        id = Profile.objects.filter(username=username).first().profile_id
        id_profile.append(id)
        model_data = MyModel.objects.all()
        # Convert the response to JSON
        json_data = content_data(f'@{username}')
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
       # Pass the data as context to the template
        user_interests = [
          ["travel", 0.9],
          ["sports", 0.7],
          ["technology", 0.8],
          ["food", 0.6]
               ]
        json_data["articles"] = sort_vlogs_by_engagement(request,json_data["articles"],user_interests)
        json_data["path"] = f'/@{username}'
        if request.method == 'POST':
        # अगर सेशन में index उपलब्ध नहीं है तो इसे प्रारंभ करें
           if 'index' not in request.session:
               request.session['index'] = 5

        # अगले 5 व्लॉग्स लाएं
           start = request.session['index']
           end = start + 5
           json_data_2 = json_data["articles"][start:end]
           request.session['index'] = end  # सेशन में index को अपडेट करें
           json_data["articles"] = json_data_2
           html = render_to_string('vlog_html.html', json_data, request=request)
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

cont_4 = []
def vlog(request, username):
    if username == request.user.username:
        print(username,request.user.username)
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            vlog_id = generate_unique_datetime_string()            
            if 'thumbnail' in request.FILES:
                uploaded_file = request.FILES['thumbnail']
                static_path = os.path.join(settings.BASE_DIR, 'static')  # Path to static/
                
                # Create the directory if it doesn't exist
                if not os.path.exists(static_path):
                    os.makedirs(static_path)

                # Generate a unique filename to prevent overwriting
                file_name = f"{vlog_id}_{uploaded_file.name}"
                file_path = os.path.join(static_path, file_name)

                # Save the file
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Generate the URL for the uploaded file
                thumbnail = f"/static/{file_name}"
                cont_4.append(thumbnail)
            
            cont_4.append(vlog_id)
            cont_4.append(title)
            cont_4.append(description)
            return render(request, 'vlog_des.html')
        else:
            return render(request, 'vlog.html')
    else:
        return HttpResponse("something wrong")

def vlogpost(request,username):
    if username == request.user.username:
       if request.method == "POST":
           vlog_id = cont_4[1]
           thumbnail = cont_4[0]
           title = cont_4[2]
           description = cont_4[3]
           data = json.loads(request.body)
           content_html = data.get('content')
           user = f'@{username}'
           vlog = Vlog(vlog_id=vlog_id,thumbnail=thumbnail,title=title,description=description,content_html=content_html,user=user)
           vlog.save()
           return render(request, 'posted.html')
       else:
           return HttpResponse("something wrong")
    else:
        return HttpResponse("something wrong")

def vlogrect(request,vlog_id):
    if Vlog.objects.filter(vlog_id=vlog_id).exists():
        model_data = MyModel.objects.all()
        # Convert the response to JSON
        vlogs = Vlog.objects.filter(vlog_id=vlog_id)
        user = Vlog.objects.get(vlog_id=vlog_id).user
        vlog_data = [{
            "title": vlog.title,
            "description": vlog.description,
            "url": f"/vlog/show/{vlog.vlog_id}",
            "urlToImage": vlog.thumbnail,
            "vlog_url": f"show/{vlog.vlog_id}",
            "publishedAt": vlog.vlog_id,                                                                                  
            "date": vlog.date_posted,
            "name": Profile.objects.get(username=user.replace('@','')).name,                 
            "profile_url": f"{vlog.user}",
            "profile_pic": Profile.objects.get(username=user.replace('@','')).profile_picture,
            "s":1
        } for vlog in vlogs]
        json_data = {"articles": vlog_data}
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

        for arti in json_data["articles"]:
           if "s" not in arti:
               arti["date"] = arti["publishedAt"]

           if UserReaction.objects.filter(vlog_id=arti["publishedAt"]).exists():
              arti["like_status"] = UserReaction.objects.get(vlog_id=arti["publishedAt"]).like
           else:
              arti["like_status"] = 0
           matching_model = model_data.filter(id=arti["publishedAt"])
     
           if UserReaction.objects.filter(username=request.user.username,follow_to=arti["profile_pic"].replace("@",'')).exists():
               arti["follow_status"] = UserReaction.objects.filter(username=request.user.username,follow_to=arti["profile_pic"].replace("@",'')).first().follow
           else:
               arti["follow_status"] = -1
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
       # Pass the data as context to the template
        return render(request, 'index.html',json_data)
    else:
        return HttpResponse("Vlog not found")

def vlogshow(request,vlog_id):
    vlog_content = Vlog.objects.get(vlog_id=vlog_id).content_html
    return render(request,'vlog_content.html',{"vlog_content":vlog_content})

def generate_unique_datetime_string():
    # Get current date and time in a specific format
    datetime_part = datetime.now().strftime("%Y%m%d%H%M%S%f")
    # Generate a unique string using UUID
    unique_string = uuid.uuid1()  # First 8 characters of UUID
    # Combine datetime and unique string
    return f"{datetime_part}-{unique_string}"

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
    profile_id = id_profile[len(id_profile)-1]  # Retrieve the profile ID from the POST request
    try:
        profile = Profile.objects.get(profile_id=profile_id)  # Fetch the profile object

        # Update profile fields
        profile.name = request.POST.get('name')

        # Handle file upload
        if 'pic' in request.FILES:
            uploaded_file = request.FILES['pic']
            static_path = os.path.join(settings.BASE_DIR, 'static')  # Path to static/uploads

            # Create the directory if it doesn't exist
            if not os.path.exists(static_path):
                os.makedirs(static_path)

            # Generate a unique filename to prevent overwriting
            file_name = f"{profile_id}_{uploaded_file.name}"
            file_path = os.path.join(static_path, file_name)

            # Save the file
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Generate the URL for the uploaded file
            file_url = f"/static/{file_name}"

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
