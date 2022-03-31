# -*- coding: utf-8 -*-

# Sample Python code for youtube.comments.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import json
import os
from pytimeparse.timeparse import timeparse
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

global youtube

def setComment(videoId, comment):
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": videoId,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment
                    }
                }
            }
        }
    )
    response = request.execute()
    return json.loads(json.dumps(response))['id']

def updateComment(id, comment):
    global youtube
    request = youtube.comments().update(
        part="snippet",
        body={
          "id": id,
          "snippet": {
            "textOriginal": comment
          }
        }
    )
    response = request.execute()

def customComment(id, comment):
    request = youtube.comments().update(
        part="snippet",
        body={
          "id": id,
          "snippet": {
            "textOriginal": "This is the updated comment."
          }
        }
    )
    response = request.execute()

def getDurationVideo(videoId):
    request = youtube.videos().list(
        part="contentDetails",
        id=videoId
    )
    response = request.execute()

    return timeparse(json.loads(json.dumps(response))['items'][0]['contentDetails']['duration'][2:])

def getVideoIds():
    file = open("videoIds", "r")
    videos = file.read().splitlines()
    return videos

def main():
    global youtube

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Settings 
    firstComment = "fisrtComment"
    secondComment = "SecondComment"
    videoIds = getVideoIds()

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)


    for videoId in videoIds:
        id = setComment(videoId, firstComment)
        print("set comment to video =", videoId)
        print("idComment =", id)
        duration = getDurationVideo(videoId)
        print("start delay with time =", duration)
        time.sleep(getDurationVideo(videoId))
        customComment(id, secondComment)
        print("update comment to video =", videoId)

if __name__ == "__main__":
    main()