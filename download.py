count=0
global ran_user
import random
from instaloader import *
from moviepy.editor import VideoFileClip
import os
import shutil

INSTAGRAM_USERNAME = "YOUR_DUMMY_USERNAME"
INSTAGRAM_PASSWORD = "YOUR_DUMMY_PASSWORD"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

downloads_dir = os.path.join(BASE_DIR, "Downloads")
video_titles_dir = os.path.join(downloads_dir, "video_titles")
username_list_txt = os.path.join(downloads_dir, "Username_list.txt")


def get_video_duration(filepath):
    clip = VideoFileClip(filepath)
    duration = clip.duration
    clip.close()
    return duration

def download_reel(username):
    try :
        os.mkdir(downloads_dir)
    except:
        pass
    os.chdir(downloads_dir)
    loader=instaloader.Instaloader()
    loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    profile = Profile.from_username(loader.context, username)
    for post in profile.get_posts():
        if post.is_video:
            loader.download_post(post, target=profile.username)

    target_directory = profile.username
    try :
        for filename in os.listdir(target_directory):
            filepath = os.path.join(target_directory, filename)
            if filename.endswith(".mp4") and get_video_duration(filepath)<59.00 or  filename.endswith(".txt"):
                pass
            else:
                os.remove(filepath)
        for filename in os.listdir(target_directory):
            filepath = os.path.join(target_directory, filename)
            if(filename.endswith(".txt")):
                try:
                    os.mkdir(video_titles_dir)
                except:
                    pass
                target = os.path.join(video_titles_dir,username)
                try:
                    os.mkdir(target)
                except:
                    pass
                shutil.copy(filepath, target)
                os.remove(filepath)
    except Exception as e:
        print(f"[ERROR] {e}")
    os.chdir(BASE_DIR)
    
def remv(ran_user):
    with open("Usernames.txt","r") as f1:
        with open("temp.txt","w") as f2:
            for line in f1:
                if (line.strip("\n")!=ran_user):
                    f2.write(line)
    os.replace("temp.txt","Usernames.txt")

def user():
    global ran_user
    with open (r"Usernames.txt","r+") as file:
        ran_user=random.choice(file.readlines()).strip()

def update_username(count):
    while (count>0):
        user()
        with open(username_list_txt, "a+") as file:
            file.write(f"{ran_user}\n")
        download_reel(ran_user)
        count=count-1
        remv(ran_user)

