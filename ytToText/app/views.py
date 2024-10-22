from django.shortcuts import render
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
from ytToText.settings import *
# Create your views here.
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
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


def register(request):
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