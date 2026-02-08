#import Connector
import upload
import download
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
downloads_dir = os.path.join(BASE_DIR, "Downloads")


def advanced():

    while True:
        user = 0
        if os.path.exists("Downloads"):
            try:
                with open(os.path.join(downloads_dir,"Username_list.txt"), "r") as f:
                    for line in f:
                        user += 1
            except:
                with open(os.path.join(downloads_dir,"Username_list.txt"), "w") as f:
                    pass
                user=0
        else:
            os.mkdir("Downloads")

        if (user >=5 ):
            upload.start()
        else:
            with open("Usernames.txt", "r") as f:
                count = 0
                lines = f.readlines()
                for line in lines:
                    count += 1
            if count < (5 - user):
                print("Please add users to Usernames.txt file")
                exit(1)
            else:
                download.update_username(5 - user)

if (__name__=='__main__'):
    mode=0
    while True:
        mode = int(input("Select A Mode\n1.User\n2.Developer\n:"))
        if mode == 1:
            print("Sorry but This Mode is still in Development")
            #Connector.conn()
        elif mode == 2:
            advanced()
        else:
            print("Invalid Choice")
