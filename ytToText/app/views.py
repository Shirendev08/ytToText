from django.shortcuts import render
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
from ytToText.settings import *
# Create your views here.
import re
import requests
from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi
from .models import ConvertedVideo



# your_app/views.py

from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate

# User registration
@api_view(['POST'])
def register_view(request):
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        # Create new user
        user = User.objects.create_user(username=username,email=email, password=password)
        return Response({"message": "User registered successfully"}, status=201)

# Custom token obtain view (login)
class MyTokenObtainPairView(TokenObtainPairView):
    pass

# Token refresh view
class MyTokenRefreshView(TokenRefreshView):
    pass

# Example of a protected view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You are authenticated!"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_video_view(request):
    video_url = request.data.get("video_url")
    if not video_url:
        return Response({"error": "Video URL is required"}, status=400)

    try:
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        converted_text = " ".join([t["text"] for t in transcript])

        converted_video = ConvertedVideo.objects.create(
            user=request.user,
            video_url=video_url,
            converted_text=converted_text
        )
        return Response({"message": "Video converted successfully", "converted_text": converted_text}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# Get conversion history
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversion_history_view(request):
    history = ConvertedVideo.objects.filter(user=request.user)
    history_data = [
        {
            "video_url": item.video_url,
            "converted_text": item.converted_text,
            "created_at": item.created_at
        }
        for item in history
    ]
    return Response({"history": history_data}, status=200)




    
    history = ConvertedVideo.objects.filter(user=request.user)
    history_data = [
        {
            "video_url": item.video_url,
            "title": item.title,
            "thumbnail_url": item.thumbnail_url,
            "converted_text": item.converted_text,
            "created_at": item.created_at
        }
        for item in history
    ]
    return Response({"history": history_data}, status=200)






@api_view(['POST', 'GET'])
def index(request):
    action = "req"
    jsons = json.loads(request.body)
    link = jsons.get('link','nokey')
    
    vid_id = link[32:43]
    print(vid_id)
    data = yta.get_transcript(vid_id,languages=['mn', 'en','ja'])

    transcript = ''
    for value in data:
        for key,val in value.items():
            if key == 'text':

                transcript += val

    l = transcript.splitlines()
    final_tra = " ".join(l)
    resp = sendResponse(request,200, f"{final_tra}", action)
    return HttpResponse(resp)


# def register(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    username = jsons['username']
    email = jsons['email']
    password = jsons['password']

    myCon = connectDB()
    cursor = myCon.cursor()
    
    query = F"""SELECT COUNT(*) AS usercount FROM t_user 
            WHERE email = '{email}' AND enabled = 1"""
    
    cursor.execute(query)
    columns = cursor.description
    respRow = [{columns[index][0]:column for index, 
        column in enumerate(value)} for value in cursor.fetchall()]
    cursor.close()

    if respRow[0]['usercount'] == 1:
        data = [{'email':email}]
        resp = sendResponse(request, 1000, data, action)
    else:
        token = generateStr(12)
        query = F"""INSERT INTO public.t_user(
	email, lastname, firstname, passw, regdate, enabled, token, tokendate)
	VALUES ('{email}', '{lastname}', '{firstname}', '{passw}'
    , NOW(), 0, '{token}', NOW() + interval \'1 day\');"""
        cursor1 = myCon.cursor()
        cursor1.execute(query)
        myCon.commit()
        cursor1.close()
        data = [{'email':email, 'firstname':firstname, 'lastname': lastname}]
        resp = sendResponse(request, 1001, data, action)
        

        sendMail(email, "Verify your email", F"""
                <html>
                <body>
                    <p>Ta amjilttai burtguulle. Doorh link deer darj burtgelee batalgaajuulna uu. Hervee ta manai sited burtguuleegui bol ene mailiig ustgana uu.</p>
                    <p> <a href="http://localhost:8001/check/?token={token}">Batalgaajuulalt</a> </p>
                </body>
                </html>
                """)

    return resp
# 