from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from app.models import MyModel
from django.db import models
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
from django.core.cache import cache
import xml.etree.ElementTree as ET
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
from django.db.models import F, FloatField, ExpressionWrapper, Value, Case, When
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

main_id = []

def robots_txt(request):
    content = """User-agent: *
Disallow:

Sitemap: https://miniview-uzfa.onrender.com/6302a139-d03a-11ef-8903-5d0b6fd2483d.xml
"""
    return HttpResponse(content, content_type="text/plain")
    
labels_list = [
    "Artificial Intelligence", "Machine Learning", "Blockchain", "Robotics", "Software Development", 
    "Cybersecurity", "Cloud Computing", "Internet of Things (IoT)", "Data Science", "Virtual Reality",
    "Football", "Cricket", "Basketball", "Tennis", "Badminton", "Athletics", "Swimming", "Baseball", 
    "Hockey", "Golf", "Fitness", "Nutrition", "Mental Health", "Yoga", "Meditation", "Healthcare Technology", 
    "Disease Prevention", "Medical Research", "Healthy Eating", "Physical Therapy", "Stock Market", "Entrepreneurship", 
    "Marketing", "E-commerce", "Venture Capital", "Cryptocurrency", "Personal Finance", "Banking", "Real Estate", 
    "Startups", "Movies", "Music", "TV Shows", "Streaming Platforms", "Celebrity News", "Video Games", "Podcasts", 
    "Animation", "Theater", "Comedy", "Online Learning", "Study Tips", "STEM Education", "Language Learning", 
    "Career Guidance", "Scholarship Opportunities", "EdTech", "Research Papers", "Public Speaking", "Writing Skills", 
    "Food", "Travel", "Fashion", "Lifestyle", "Parenting", "Art", "Photography", "Design", "Architecture", 
    "Cooking", "Gardening", "Home Improvement", "DIY", "Sports Science", "Psychology", "Sociology", "Philosophy", 
    "Literature", "History", "Politics", "Economics", "Law", "Social Media", "Technology News", "Gaming", 
    "Mobile Apps", "Entrepreneurship Tips", "Productivity", "Self-Improvement", "Leadership", "Public Relations", 
    "Digital Marketing", "Influencer Marketing", "Advertising", "Event Planning", "Human Resources", "Workplace Culture", 
    "Customer Service", "Retail", "Food Industry", "Manufacturing", "Automotive", "Transportation", "Logistics", 
    "Supply Chain", "Sustainability", "Renewable Energy", "Climate Change", "Environmentalism", "Wildlife", "Oceanography", 
    "Astronomy", "Space Exploration", "Physics", "Chemistry", "Biology", "Genetics", "Medicine", "Healthcare Innovation", 
    "Medical Devices", "Drug Development", "Healthcare Policy", "Public Health", "Social Justice", "Human Rights", 
    "Diversity", "Equality", "Immigration", "International Relations", "Globalization", "UN", "NGOs", "Peacekeeping", 
    "Conflict Resolution", "Cyberbullying", "Mental Health Awareness", "Addiction", "Recovery", "Grief", "Trauma", 
    "Coping Mechanisms", "Therapy", "Coaching", "Life Coaching", "Nutrition Science", "Fitness Plans", "Well-being", 
    "Chronic Illness", "Public Speaking Tips", "Career Development", "Job Search", "Interview Skills", "Resume Writing", 
    "Entrepreneurship Courses", "Coding", "Web Development", "App Development", "UI/UX Design", "Data Analytics", 
    "Cloud Services", "Game Development", "Artificial Neural Networks", "Speech Recognition", "Natural Language Processing", 
    "Computer Vision", "Automation", "Robotic Process Automation", "Autonomous Vehicles", "Smart Cities", "Electric Vehicles", 
    "Renewable Resources", "Smart Grid", "Cybersecurity Threats", "Identity Protection", "Privacy", "Digital Footprint", 
    "Online Privacy", "Data Protection", "Blockchain Security", "Ethical Hacking", "Cryptography", "IoT Security", 
    "Digital Transformation", "SaaS", "PaaS", "Cloud Migration", "Edge Computing", "AI Ethics", "AI Regulation", 
    "Tech Startups", "FinTech", "HealthTech", "EdTech", "E-learning", "GreenTech", "AgTech", "LegalTech", 
    "IoT Devices", "Wearable Tech", "Smart Home", "AI in Healthcare", "AI in Education", "AI in Finance", 
    "AI in Business", "AI in Marketing", "AI in Transportation", "AI in Manufacturing", "Machine Vision", "Speech Synthesis", 
    "Image Recognition", "Natural Language Generation", "Deep Learning", "Reinforcement Learning", "Supervised Learning", 
    "Unsupervised Learning", "Neural Networks", "Support Vector Machines", "Decision Trees", "Random Forests", 
    "K-means Clustering", "Logistic Regression", "Regression Analysis", "Bayesian Inference", "Time Series Analysis", 
    "Data Visualization", "Big Data", "Data Mining", "Data Engineering", "Predictive Modeling"
]

def custom_sitemap(request):
    # Root XML element
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    static_urls = [
    {'loc': 'https://miniview-uzfa.onrender.com/', 'lastmod': '2025-01-11', 'changefreq': 'daily', 'priority': '1.0'},  # Home page
    {'loc': 'https://miniview-uzfa.onrender.com/view', 'lastmod': '2025-01-11', 'changefreq': 'weekly', 'priority': '0.8'},  # View page
    {'loc': 'https://miniview-uzfa.onrender.com/about', 'lastmod': '2025-01-11', 'changefreq': 'monthly', 'priority': '0.7'},  # About page
    {'loc': 'https://miniview-uzfa.onrender.com/login', 'lastmod': '2025-01-11', 'changefreq': 'monthly', 'priority': '0.6'},  # Login page
    {'loc': 'https://miniview-uzfa.onrender.com/signup', 'lastmod': '2025-01-11', 'changefreq': 'monthly', 'priority': '0.6'},  # Signup page
    {'loc': 'https://miniview-uzfa.onrender.com/search', 'lastmod': '2025-01-11', 'changefreq': 'weekly', 'priority': '0.7'},  # Search page
    {'loc': 'https://miniview-uzfa.onrender.com/coment', 'lastmod': '2025-01-11', 'changefreq': 'daily', 'priority': '0.8'},  # Comment page
    {'loc': 'https://miniview-uzfa.onrender.com/top/trending', 'lastmod': '2025-01-11', 'changefreq': 'daily', 'priority': '0.8'},  # Add comment page
    {'loc': 'https://miniview-uzfa.onrender.com/top/topblog', 'lastmod': '2025-01-11', 'changefreq': 'weekly', 'priority': '0.7'},  # Comment count page
]

    # Add static URLs to the sitemap
    for url in static_urls:
        url_elem = ET.SubElement(urlset, 'url')
        ET.SubElement(url_elem, 'loc').text = url['loc']
        ET.SubElement(url_elem, 'lastmod').text = url['lastmod']
        ET.SubElement(url_elem, 'changefreq').text = url['changefreq']
        ET.SubElement(url_elem, 'priority').text = url['priority']

    # Dynamic URLs from database (users and vlogs)
    users = User.objects.all()
    vlogs = Vlog.objects.all()

    # Add dynamic user profile URLs
    for user in users:
        url_elem = ET.SubElement(urlset, 'url')
        ET.SubElement(url_elem, 'loc').text = f'https://miniview-uzfa.onrender.com/@{user.username}'
        ET.SubElement(url_elem, 'lastmod').text = '2025-01-11'
        ET.SubElement(url_elem, 'changefreq').text = 'daily'
        ET.SubElement(url_elem, 'priority').text = '0.7'

    # Add dynamic vlog URLs
    for vlog in vlogs:
        url_elem = ET.SubElement(urlset, 'url')
        ET.SubElement(url_elem, 'loc').text = f'https://miniview-uzfa.onrender.com/vlog/show/{vlog.vlog_id}'
        ET.SubElement(url_elem, 'lastmod').text = '2025-01-11'
        ET.SubElement(url_elem, 'changefreq').text = 'weekly'
        ET.SubElement(url_elem, 'priority').text = '0.6'

    # Convert XML to string
    xml_content = ET.tostring(urlset, encoding='utf-8', method='xml')

    # Serve the XML directly as the response
    return HttpResponse(xml_content, content_type='application/xml')

def check_and_delete(file_name, dir_path):
    file_path = os.path.join(dir_path, file_name)
    
    # Check if file exists
    if os.path.exists(file_path):
        print(f"File '{file_name}' found. Deleting it...")
        os.remove(file_path)  # Delete the file
        
def average_labels(input_array):
    # Dictionary to store the total score and count for each label
    label_data = {}

    for label, score in input_array:
        if label in label_data:
            label_data[label]['total'] += score
            label_data[label]['count'] += 1
        else:
            label_data[label] = {'total': score, 'count': 1}

    # Calculate average for each label and prepare the result
    result = [[label, round(data['total'] / data['count'], 2)] for label, data in label_data.items()]
    return result

def get_top_vlogs(request, username,LIKE_WEIGHT,VIEW_WEIGHT,COMMENT_WEIGHT,RECENCY_WEIGHT,num):
    # Step 1: Fetch user's interest labels and weights
    user_interest = []
    if UserReaction.objects.filter(username=request.user.username).exists():
        user_interest = [
            (reaction.user_interest, reaction.interest_rate)
            for reaction in UserReaction.objects.filter(username=request.user.username)
        ]

    # Convert user interests to a dictionary
    interest_dict = {label: weight for label, weight in user_interest}

    # Step 2: Define dynamic category weight case
    category_weight_case = Case(
        *[
            When(vlog_labels=label, then=Value(weight))
            for label, weight in interest_dict.items()
        ],
        default=Value(1.0),  # Default weight if no match found
        output_field=FloatField()
    )

    # Step 3: Annotate vlogs with calculated fields
    vlogs = Vlog.objects.annotate(
        category_weight=category_weight_case,
        base_engagement_score=ExpressionWrapper(
            (F('likes') * LIKE_WEIGHT) +
            (F('views') * VIEW_WEIGHT) +
            (F('comment') * COMMENT_WEIGHT),
            output_field=FloatField()
        )
    )[:num]

    # Step 4: Calculate final engagement score including recency
    top_vlogs = []
    for vlog in vlogs:
        # Ensure vlog date is timezone-aware
        vlog_date_posted = vlog.date_posted if vlog.date_posted.tzinfo else vlog.date_posted.replace(tzinfo=now().tzinfo)

        # Calculate recency score
        recency_seconds = (now() - vlog_date_posted).total_seconds()
        recency_days = recency_seconds / 86400  # Convert seconds to days
        recency_score = 1.0 / (recency_days + 1)  # Add 1 to avoid division by zero

        # Final engagement score
        vlog.engagement_score = (
            vlog.base_engagement_score * vlog.category_weight +
            (recency_score * RECENCY_WEIGHT)
        )
        top_vlogs.append(vlog)

    # Step 5: Sort vlogs by engagement score in descending order
    top_vlogs = sorted(top_vlogs, key=lambda x: x.engagement_score, reverse=True)

    # Debugging Output
    for vlog in top_vlogs:
        print(f"Vlog ID: {vlog.vlog_id}, Likes: {vlog.likes}, Views: {vlog.views}, Comments: {vlog.comment}")
        print(f"Base Score: {vlog.base_engagement_score}, Recency Score: {recency_score}, Final Score: {vlog.engagement_score}")

    return top_vlogs

def content_data(request,user_2,arr):
    if user_2 == 'all':
        vlogs = get_top_vlogs(request,request.user.username,arr[0],arr[1],arr[2],arr[3],arr[4])
        vlog_data = [{
            "title": vlog.title,
            "description": vlog.description,
            "url": f"vlog/show/{vlog.vlog_id}" if os.path.exists("path/to/file_or_dir") else str(vlog.objects.get(vlog_id=vlog_id).content_html),
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
            "url": f"vlog/show/{vlog.vlog_id}" if os.path.exists("path/to/file_or_dir") else str(vlog.objects.get(vlog_id=vlog_id).content_html),
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

def home(request):
    model_data = MyModel.objects.all()
    json_data = content_data(request,'all',[0.3,0.2,0.6,0.4,10])
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

def most(request,para):
    if para == "topblog":
        arr = [0.4,0.3,0.7,0.3,10]
    elif para == "trending":
        arr = [0.3,0.5,0.7,0.5,10]
    else:
        return redirect('/')
    model_data = MyModel.objects.all()
    json_data = content_data(request,'all',arr)
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
    json_data["articles"][-1]["end"] = 1
    json_data["path"] = '/'
    if request.method == 'POST':
        if 'index' not in request.session:
            request.session['index'] = 6
        start = request.session['index']
        end = start + 5
        json_data_2 = json_data["articles"][start:end]
        request.session['index'] = end  
        json_data["articles"] = json_data_2
        html = render_to_string('vlog_html.html', json_data, request=request)
        return JsonResponse({'html': html})
    else:
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

def searchquary(request):
    if request.method == 'POST':
        quary = request.session.get('last_quary', '')  # Retrieve the last query from the session
    else:
        quary = request.GET.get('quary', '')  # Get the query from the request
        request.session['last_quary'] = quary  # Save the query in the session

    # Fetch content data
    json_data = content_data(request, 'all', [0.3, 0.2, 0.6, 0.4, 10])
    model_data = MyModel.objects.all()

    # Convert the response to JSON
    json_data["articles"] = [
        article for article in json_data.get("articles", []) 
        if article.get("title") != "[Removed]"
    ]
    json_data["articles"] += content_data('all')["articles"]

    # Add user profile information if available
    if request.user.is_authenticated:
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

    # Process articles
    for arti in json_data.get("articles", []):
        if "s" not in arti:
            arti["date"] = arti.get("publishedAt", "")
            arti["name"] = Profile.objects.get(username='justwatch').name
            arti["profile_url"] = "@justwatch"
            arti["profile_pic"] = Profile.objects.filter(username='justwatch').first().profile_picture

        arti["like_status"] = (
            UserReaction.objects.filter(vlog_id=arti.get("publishedAt"))
            .values_list('like', flat=True)
            .first() or 0
        )

        arti["follow_status"] = (
            UserReaction.objects.filter(
                username=request.user.username,
                follow_to=arti.get("profile_pic", "").replace("@", ""),
            )
            .values_list('follow', flat=True)
            .first() or -1
        )

        matching_model = model_data.filter(id=arti.get("publishedAt"))
        arti["views"] = matching_model.values_list('views', flat=True).first() or 0
        arti["likes"] = matching_model.values_list('likes', flat=True).first() or 0

        if comentconfig.objects.filter(mainid=arti.get("publishedAt")).exists():
            data = comentconfig.objects.filter(mainid=arti["publishedAt"])
            arti["coment"] = data.count()
        else:
            arti["coment"] = 0

    # Perform fuzzy search on articles
    inverted_index = build_inverted_index(json_data["articles"])
    json_data["articles"] = fuzzy_search(quary, inverted_index, json_data["articles"])
    json_data["articles"][-1]["end"] = 1
    json_data["path"] = '/search/quary'

    # Handle pagination
    if request.method == 'POST':
        start = request.session.get('index', 6)
        end = start + 5
        json_data_2 = json_data["articles"][start:end]
        request.session['index'] = end

        html = render_to_string('vlog_html.html', {'articles': json_data_2}, request=request)
        return JsonResponse({'html': html})
    else:
        request.session['index'] = 6
        json_data_4 = json_data["articles"][:6]
        return render(request, 'index.html', {'articles': json_data_4})


def extract_contextual_keyword(text, labels):
    # Generate keywords from labels (basic assumption: labels as keywords)
    label_keywords = {label: [label] for label in labels}
    
    # Create corpus from generated label keywords
    corpus = [" ".join(keywords) for keywords in label_keywords.values()]
    
    # Initialize vectorizer and fit corpus
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Vectorize the input text
    query_vec = vectorizer.transform([text])
    
    # Compute cosine similarity between query and label keywords
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Find the label with the highest similarity score
    max_index = similarities.argmax()
    most_related_label = labels[max_index]
    highest_similarity_score = similarities[max_index]
    
    return [most_related_label, highest_similarity_score]
    
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
            "user_interest":extract_contextual_keyword(Vlog.objects.get(vlog_id=id).title,labels_list)[0],
            "interest_rate":extract_contextual_keyword(Vlog.objects.get(vlog_id=id).title,labels_list)[1]
        }
       
    )
    vlog = Vlog.objects.get(vlog_id=id)
    vlog.likes = status[0]
    vlog.views = status[1]
    vlog.save()
    model = MyModel(id=id,views=status[0],likes=status[1])
    model.save()
    return HttpResponse("something wrong")

def coment(request):
    if request.method == 'POST':
        id = request.POST.get("mainid")
        main_id.append(id)
        data = comentconfig.objects.filter(mainid=id)
        # Serialize the queryset to JSON
        vlog = Vlog.objects.get(vlog_id=id)
        vlog.comments = len([a for a in data])
        vlog.save()
        serialized_data = serialize('json', data)
        
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
   json_data = content_data(request,'all',[0.3,0.2,0.6,0.4,10])
   return render(request, 'search.html', {"search":[vlog["title"] for vlog in json_data["articles"]}) 

def about(request):
   return render(request, 'about.html') 
    
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
            return render(request, 'login.html', {'error': "Invalid email or password."})

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

                file_name = f"thumbnail_{vlog_id}"
                check_and_delete(file_name, '/media')
                file_path = os.path.join(static_path, file_name)

                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

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

def vlogpost(request, username):
    if username == request.user.username:
        if request.method == "POST":
            try:
                draft_vlog = DraftVlog.objects.get(user=request.user)
            except DraftVlog.DoesNotExist:
                return HttpResponse("No draft found")

            data = json.loads(request.body)
            content_html = data.get('content')

            directory_path = os.path.join(settings.MEDIA_ROOT, 'vlog/')
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            file_path = f'{directory_path}{draft_vlog.vlog_id}.html'
            with open(file_path, 'w') as file:
                file.write(content_html)

            user = f'@{username}'
            vlog_labels = extract_contextual_keyword(draft_vlog.title, labels_list)[0]
            vlog_rate = extract_contextual_keyword(draft_vlog.title, labels_list)[1]

            vlog = Vlog(
                vlog_id=draft_vlog.vlog_id,
                thumbnail=draft_vlog.thumbnail,
                title=draft_vlog.title,
                description=draft_vlog.description,
                user=user,
                content_html=content_html,
                vlog_labels=vlog_labels,
                vlog_rate=vlog_rate,
            )
            vlog.save()

            # Delete the draft
            draft_vlog.delete()

            return HttpResponse("Published")
        else:
            return HttpResponse("Something went wrong")
    else:
        return HttpResponse("Something went wrong")


def media(request,index):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']  # Corrected key for the file
        static_path = os.path.join(settings.BASE_DIR, 'media')  # Path to media/
        
        # Create the directory if it doesn't exist
        if not os.path.exists(static_path):
            os.makedirs(static_path)

        # Generate a unique filename to prevent overwriting
        file_name = f"vlog_{cont_4[1]}_{index}"  # Added file extension (.jpg)
        
        # Check and delete the file if it exists
        check_and_delete(file_name, '/media')

        # Define the file path
        file_path = os.path.join(static_path, file_name)

        # Save the file
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Generate the URL for the uploaded file
        thumbnail_url = f"/media/{file_name}"

        return JsonResponse({"thumbnail_url": thumbnail_url}, status=200)

    return JsonResponse({"error": "No file found"}, status=400)
    
def api(request,thumbnail,title,description,user,content_html):
    vlog_id = generate_unique_datetime_string()
    vlog_labels = extract_contextual_keyword(title,labels_list)[0]
    vlog_rate = extract_contextual_keyword(title,labels_list)[1]
    vlog = Vlog(vlog_id=vlog_id,thumbnail=thumbnail,title=title,description=description,user=user,content_html=content_html,vlog_labels=vlog_labels,vlog_rate=vlog_rate)
    vlog.save()
    return HttpResponse("post done")

def vlogrect(request,vlog_id):
    if Vlog.objects.filter(vlog_id=vlog_id).exists():
        model_data = MyModel.objects.all()
        # Convert the response to JSON
        vlogs = Vlog.objects.filter(vlog_id=vlog_id)
        user = Vlog.objects.get(vlog_id=vlog_id).user
        vlog_data = [{
            "title": vlog.title,
            "description": vlog.description,
            "url": f"vlog/show/{vlog.vlog_id}" if os.path.exists("path/to/file_or_dir") else str(vlog.objects.get(vlog_id=vlog_id).content_html),
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

def vlogshow(request, vlog_id):
    cache_key = f"vlog_content_{vlog_id}"
    vlog_content = cache.get(cache_key)  # Cache se content retrieve karna
    user = Vlog.objects.get(vlog_id=vlog_id).user.split('@')[1]
    profile = Profile.objects.get(username=user)
    userrection = UserReaction.objects.filter(username=request.user.username, follow_to=f'@{user}').first()
    if userrection:
       follow_status = userrection.follow
    else:
       follow_status = -1

    if not vlog_content:  # Agar cache mein content na ho
        file_path = os.path.join(settings.MEDIA_ROOT, f"vlog/{vlog_id}.html")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                vlog_content = file.read()
                cache.set(cache_key, vlog_content, timeout=300)  # Cache mein store karna (5 minutes timeout)
        except FileNotFoundError:
            vlog_content = "<h1>Content not found</h1>"
    return render(request, 'vlog_content.html', {"vlog_content": vlog_content,"name":profile.name,"username":profile.username,"pic":profile.profile_picture,"title":Vlog.objects.get(vlog_id=vlog_id).title,"id":profile.profile_id,"follow":follow_status,"vlog_id":vlog_id})
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
