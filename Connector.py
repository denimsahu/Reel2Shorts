import os
import experiment
import upload
import instaloader
import download
import instaloader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
downloads_dir = os.path.join(BASE_DIR, "Downloads")
video_titles_dir = os.path.join(downloads_dir, "video_titles")
username_list_txt = os.path.join(downloads_dir, "Username_list.txt")


def remove(username):
    os.remove(os.path.join(downloads_dir,username))
    try:
        os.remove(os.path.join(video_titles_dir,username))
    except:
        pass
def conn():
    downl=0
    while True:
        downl=input("How many users profile you wish to download and use? \nBy default its set to 5 \nPress Enter to continue: ")
        if(downl==""):
            downl=5
            break
        elif(downl==1-1000):
            break
        else:
            print("Invalid Input")


    while True:
        new_username=input("Do you wish to add new usernames to username list?\n(you can add multiple usernames to username.txt file directly yourself)\nYes/No(Press Enter): ")
        if new_username.lower()=="yes":
            username=input("Enter username: ")
            if(username==""):
                print("Please enter an username")
            else:
                bot = instaloader.Instaloader()
                try:
                    profile = instaloader.Profile.from_username(bot.context, username)
                except:
                    print("Username does'nt exists")
                else:
                    if (profile.is_private == True):
                        print("profile is private")
                    elif (profile.is_private == False):
                        with open("Usernames.txt", "a+") as file:
                            file.write(f"\n{username}")

        elif new_username.lower()=="no" or new_username=="":
            break
        else:
            print("Please choose an valid option")
    while True:
        del_user = input("Do you wish to delete existing users videos from database?\nYes/No(Press Enter): ")
        if del_user.lower() == "yes":
            username=""
            username = input("Enter username: ")
            if username=="":
               print("Please enter an username")
            else:
                exists=False
                with open (username_list_txt,"r") as file:
                    lines=file.readlines()
                    for line in lines:
                        print(line)
                        if(line.strip()==username):
                            exists=True
                if(exists==True):
                    with open (username_list_txt,"r") as f:
                        lines = f.readlines()
                        with open (username_list_txt,"w") as f:
                            for line in lines:
                                if (line.strip("\n") != username):
                                    f.write(line)
                    remove(username)
                else:
                    print("This username doesn't exist in our database")

        elif del_user.lower() == "no" or del_user == "":
            break
        else:
            print("Please choose an valid option")
    while True:
        user = 0
        try:
            with open (username_list_txt,"r") as f:
                for line in f:
                    user=user+1
        except:
            pass
        if(user==downl):
            experiment.upload_video()
        else:
            with open("Usernames.txt", "r") as f:
                count = 0
                lines = f.readlines()
                for line in lines:
                    count = count + 1
                if (count<(downl-user)):
                    print(f"Please add users to Usernames.txt file")
                    break
            download.update_username(downl-user)
