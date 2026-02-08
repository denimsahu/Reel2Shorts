import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import json
import os
import random
import time
from datetime import datetime
from google.oauth2.credentials import Credentials
import psutil

client_secreat_keys_line = 0
client_quota = 0
username = ""
video_name = ""
secreat_key = ""
youtube = ""
title = " "
eligible_del=0
youtube=""

def select_profile():
    global username
    with open("Downloads\\Username_list.txt", "r") as file:
        username = random.choice(file.readlines()).strip()


def select_video(username):
    global video_name
    video_name = random.choice(os.listdir(f"Downloads\\{username}"))


def get_client_secreat_file():
    global client_quota, client_secreat_keys_line, secreat_key
    try:
        client_quota = 0
        client_secreat_keys_line = client_secreat_keys_line + 1
        with open("client_secreat_keys", "r") as file:
            secreat_key = file.readlines()[client_secreat_keys_line].strip()
        return secreat_key
    except:
        print("""
used quota of all exisiting projects!!
create new project and downloaded them and add there secreat key json file to secreat_keys folder in this project,
and add there file name to client_secreat_keys.txt file.
Entering Into 2 Hour Cooldown Period.
        
        
                                                                    ADIOS!!
""")
        client_secreat_keys_line = 0
        print(datetime.now().strftime("%d-%m-%Y %I:%M %p"))
        time.sleep(7200)
        upload_setup()


def upload_setup():
    client_secrets_file = get_client_secreat_file()
    scopes = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

    # Check if authorization credentials already exist
    credentials_file = f'secreat_keys_credentials\credentials_{client_secrets_file}.json'
    if os.path.exists(credentials_file):
        # Load the stored credentials
        with open(credentials_file, 'r') as f:
            credentials_data = json.load(f)
        credentials = Credentials.from_authorized_user_info(credentials_data, scopes)
    else:
        # Create the flow instance and initiate the OAuth 2.0 authorization process
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(f"secreat_keys\\{client_secrets_file}", scopes)
        credentials = flow.run_local_server(port=5051)
        credentials.expiry = None
        # Store the authorization credentials for future use
        if os.path.exists("secreat_keys_credentials"):
            with open(credentials_file, 'w') as f:
                f.write(credentials.to_json())
        else:
            os.mkdir("secreat_keys_credentials")
            with open(credentials_file, 'w') as f:
                f.write(credentials.to_json())


    # Create a YouTube API client
    global youtube
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
    upload_video(credentials_file)


def generate_video_title():
    tags = ['quotes', 'gaming', 'music', 'travel', 'motivation', "feelings", "shorts"]
    max_length = 100
    hashtags = ' '.join(['#' + tag for tag in tags])
    title = ' '.join([random.choice(tags) for _ in range(random.randint(3, 6))])
    title = title.capitalize()
    if len(title) + len(hashtags) <= max_length:
        return title + ' ' + hashtags
    else:
        return generate_video_title()


def upload_video(credentials_file="null"):
    global client_quota, video_name, username, title,eligible_del
    if (title == " "):
        try:
            with open(f"Downloads\\video_titles\\{username}\\{video_name[:-4]}.txt", "r+", encoding="utf-8") as file:
                title = file.readlines()
            title = title[0]
        except:
            title = generate_video_title()
    try:
        request_body = {
            'snippet': {
                'title': title,
                'description': 'credits to the owner on instagram: @'+username,
                'tags': ['minecraft', 'gta5'],
                'categoryId': '22'  # The category ID for your video (e.g., '22' for Entertainment)
            },
            'status': {
                'privacyStatus': 'public'  # Set the privacy status of the video
            }
        }
        # Upload the video
        media = MediaFileUpload(f"Downloads\\{username}\\{video_name}")
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()

        # Print the response
        print('Video uploaded! Video ID:', response['id'])
        eligible_del = 1
        print(f"{username}\\{video_name}")
        print(title)
        title = " "
        print(datetime.now().strftime("%d-%m-%Y %I:%M %p"))
        client_quota = client_quota + 1

        while True:
            status_response = youtube.videos().list(
                part='status',
                id=response['id']
            ).execute()
            upload_status = status_response['items'][0]['status']['uploadStatus']
            #print(upload_status)
            if upload_status == 'processed':
                break
            else:
                time.sleep(5)  # Wait for 5 seconds before checking again

            # Video upload is complete, continue with other operations
        print('Video upload complete!')

    except Exception as e:
        error_message = str(e)
        if "The user has exceeded the number of videos they may upload." in error_message:
            # Handling upload limit error
            print("you have exceeded the number of video you can upload from a youtube account\nGoing into 2 hour COOLDOWN")
            print(datetime.now().strftime("%d-%m-%Y %I:%M %p"))
            time.sleep(7200)
            upload_video()

        elif "Unable to find the server at oauth2.googleapis.com" in error_message:
            # Handling internet connection error
            print("Can't connect to the internet. Please check your internet connectivity,retying after sometime.")
            print(datetime.now().strftime("%d-%m-%Y %I:%M %p"))
            time.sleep(300)
            upload_video()

        elif '<HttpError 400 when requesting https://youtube.googleapis.com/upload/youtube/v3/videos?part=snippet%2Cstatus&alt=json&uploadType=multipart returned "The request metadata specifies an invalid or empty video title."' in error_message:
            # Handling invalid or empty video title error
            print(error_message)
            print("Invalid title!!")
            print(title)
            if title != f"video {title.replace('video ','')}":
                title = "video " + title
                upload_video()
            elif(title==f"video {title.replace('video ','')}"):
                title = generate_video_title()
                upload_video()

        elif "quota" in error_message.lower():
            # Handling quota error
            global client_secreat_keys_line
            print(error_message)
            print("You have used the full quota of this project. Switching project to upload video....")
            upload_setup()

        elif "invalid_grant" in error_message.lower():
            os.remove(credentials_file)
            client_secreat_keys_line = 0
            upload_setup()

        else:
            # Handling other exceptions
            print("An error occurred:", error_message)
            title=" "
            print(title)
            print(f"{username}\{video_name}")
            upload_video()

def is_file_in_use(file_path):
    # Check if a file is still being accessed by another process
    try:
        for proc in psutil.process_iter(['pid', 'open_files']):
            try:
                open_files = proc.info.get('open_files')
                if open_files and any(file_path == info.path for info in open_files):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Ignore processes that no longer exist or raise AccessDenied
                pass
    except psutil.Error:
        # Ignore any other psutil errors
        pass

    return False
def del_video(username, video_name):
    global eligible_del, youtube
    eligible_del = 0
    retry_count = 0
    max_retries = 5
    #time.sleep(120)
    while retry_count < max_retries:
        try:
            os.remove(f"Downloads\\{username}\\{video_name}")
            try:
                os.remove(f"Downloads\\video_titles\\{username}\\{video_name[:-4]}.txt")
            except:
                pass
            finally:
                print(f"{username}\\{video_name} \nvideo deleted")
                retry_count=5
        except Exception as e:
            print("Some error occurred, video cannot be deleted!! \n", e)
            if is_file_in_use(f"Downloads\\{username}\\{video_name}"):
                retry_count += 1
                print(f"File is still in use. Retrying in 10 seconds... (Retry {retry_count}/{max_retries})")
                time.sleep(10)
            else:
                print("File is no longer in use. Exiting the deletion process.")
                break

    if retry_count >= max_retries:
        print("Failed to delete the file after multiple retries. Skipping deletion.")

    if (os.listdir(f"Downloads\\{username}") == []):
        del_user(username)



def del_user(username):
    with open(r"Downloads\Username_list.txt", "r") as f:
        lines = f.readlines()
    with open(r"Downloads\Username_list.txt", "w") as f:
        for line in lines:
            if (line.strip("\n") != username):
                f.write(line)
    os.rmdir(f"Downloads\{username}")
    try:
        os.remove(f"Downloads\\video_titles\\{username}")
    except:
        pass


def beginning():
    select_profile()
    select_video(username)
    upload_video()


def new_beginning():
    select_profile()
    select_video(username)
    upload_setup()

def main_del():
    del_video(username, video_name)
    count=0
    time.sleep(300)

def start():
    new_beginning()
    if eligible_del==1:
        main_del()
    while True:
        if client_quota < 5:
            beginning()
            if eligible_del == 1:
                main_del()
        elif client_quota == 5:
            new_beginning()
            if eligible_del == 1:
                main_del()
