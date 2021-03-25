# **SETUP**

**Prerequisites**
- A Linux distro
- An up to date install of Docker. More information here: https://docs.docker.com/engine/install/
> You will need to run docker without having to use sudo.To do this run the following:<br>
``sudo groupadd docker``<br>
``sudo usermod -aG docker $USER``<br>
You will need to log out and log back in so your user membership is reevaluated.

- A version of python installed that is between 3.5 and 3.9

* **Step 1** <br>
Clone the repo using: <br>
``
git clone link
``

* **Step 2** <br>
Run the setup script in the cs14-main folder: <br>
``
python setup.py
``
If you do this, you can skip to **Step 5**.
Alternatively, or if this script fails, do the following steps.<br>

* **Step 3** <br>
Install the requirements. <br>
CD into the cloned directory and use the following command: <br>
``
pip install -r requirements.txt
``

* **Step 4** <br>
Create the database. <br>
CD into the "main" directory and run the following commands.<br>
``
python manage.py makemigrations `` <br>
``
python manage.py makemigrations cs14 `` <br>
``
python manage.py migrate
``

* **Step 5** (optional)<br>
Populate the database. <br>
Run the following populate command <br>
``
python manage.py loaddata db.json
``

* **Step 6** <br>
Create a django admin user to manage site. <br>
Run the following terminal command <br>
``
python manage.py createsuperuser
``

* **Step 7**<br>
Setup the docker image.<br>
Run the following terminal command <br>
``
docker build -t coding-image .
``<br>
> Note: The docker image may take a few minutes to build.

* **Step 8** <br>
Run the site. <br>
Run the following terminal command <br>
``
python manage.py runserver
``

Thats it, the local version of the site should now be up and running. You can add administrator users and reviews from the django admin panel. Administrators can then generate user accounts for candidates.

# **ADMIN**
Stuff about adding users. Will update this section once we have the two database dumps.

# **ADDING CODING TASKS**
Tasks can be added via the Django admin interface, however, the expected output and sample input need to be added manually. To do so:
* Create a directory in cs14-main/main/media/tests/ with the name test followed by the the task id. For example, if the task id is 1, the folder should be named "test1".
* Within this new directory, create two directories: input and output.
* In the input folder, create a file containing the input to the code. If no input is required, create an empty file, input.txt.
* In the output folder, create a file containing the expected output of the code.

# **ADDING MORE LANGUAGES**
If you want to add more languages, you will need to:
* Add installation instructions for the compiler/language in the Dockerfile, which can be found in cs14-main/main/static/python/
* Add code for compilation and/or running in runcontainer.py, found in cs14-main/main/static/python/
* Rebuild the Docker image
* Add the necessary file extension in the add_language_extension function found in compile.py (cs14-main/main/static/python)
