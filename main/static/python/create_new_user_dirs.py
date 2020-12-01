from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent


MEDIA_DIR = os.path.join(BASE_DIR,'media')
USER_DIR = os.path.join(MEDIA_DIR, 'users')


def create_new_user(username):
    try:
        new_user_dir = os.path.join(USER_DIR, username)
        os.mkdir(new_user_dir)
    except:
        print('Cant create user folder')


create_new_user('MarkHarris')


    

