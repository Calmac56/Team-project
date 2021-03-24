import subprocess
import os

#INSTALL REQUIREMENTS
installation, error = subprocess.Popen(["pip", "install", "-r", "requirements.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
if len(error)!=0:
    print("Error installing requirements.", error)

#CREATE DATABASE
db, error = subprocess.Popen(["python", "manage.py", "makemigrations"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
if len(error)!=0:
    print("Error making migrations.", error)

db, error = subprocess.Popen(["python", "manage.py", "migrate"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
if len(error)!=0:
    print("Error migrating to database.", error)

#BUILD DOCKER IMAGE
error = "initial"
iterations = 0
cwd = os.getcwd()
while len(error) != 0:
    build = subprocess.Popen(["docker", "build", "-t", "coding-image", "."], cwd=os.path.join(cwd,"main", "static", "python"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = build.communicate()
    if iterations == 4:
        print("Build failed too many times")
        break
    iterations += 1
