from django.shortcuts import render
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
from ytToText.settings import sendResponse
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

# @api_view(['POST', 'GET'])
# def bookadd(request):
#     action = 'bookadd'
#     jsons = json.loads(request.body)
#     bname = jsons.get('bname','nokey')
#     author = jsons.get('author','nokey')
#     btype = jsons.get('btype','nokey')
   
#     con = connect()
#     cursor = con.cursor()

#     try: 
#         cursor.execute(f"SELECT * FROM t_book WHERE bname = '{bname}' AND author = '{author}' AND btype = '{btype}'")
#         existing_bookadd = cursor.fetchone()
#         if existing_bookadd:
#             resp = sendResponse(request,400, f"{bname} ном бүртгэгдсэн байна", action)
#         else:
#             cursor.execute(f"""INSERT INTO t_book(bname, author, btype) VALUES('{bname}', '{author}', '{btype}')""")
#             con.commit()
#             resp= sendResponse(request,200, f"{bname} номыг бүртгэлээ", action)

#         return HttpResponse(resp)
#     except Exception as e:
#         # Handle database errors
#         error_message = "Database error: " + str(e)
#         resp = sendResponse(request,500, error_message, action)
#         return HttpResponse(resp)