# **SETUP**

**Prerequisites**
1. A Linux distro - we have been using Ubuntu.
2. An up-to-date installation of Docker. More information here: https://docs.docker.com/engine/install/
> You will need to run docker without having to use sudo. To do this, run the following in the terminal:<br>
<br>``sudo groupadd docker``<br>
``sudo usermod -aG docker $USER``<br>
<br>You will likely need to log out and log back in so your user membership is reevaluated.

3. A version of Python that is between 3.5 and 3.9.

<br>

* **Step 1** <br>
Clone the repo using: https://github.com/Calmac56/Team-project.git <br>
``
git clone <link>
``

* **Step 2** <br>
Run the setup script in the cs14-main/ directory: <br>
``
python setup.py
``
If you do this, you can skip to **Step 5**.
Alternatively, or if this script fails, do the following steps.<br>

* **Step 3** <br>
Install the requirements. <br>
In the cs14-main/ directory, run: <br>
``
pip install -r requirements.txt
``

* **Step 4** <br>
Create the database. <br>
In the cs14-main/main/ directory, run the following commands: <br>
``
python manage.py makemigrations `` <br>
``
python manage.py makemigrations cs14 `` <br>
``
python manage.py migrate
``

* **Step 5** (optional)<br>
Populate the database. <br>
We have provided two database dumps, admindb.json and exampledb.json in the cs14-main/main directory. The first one simply contains a superuser, which does not yet have any site privileges assigned, they simply have access to the Django admin interface.<br>
The second contains a superuser with site admin and reviewer privileges (can generate users, tasks and review tasks), a candidate and two tasks, both assigned to the candidate. <br>
You can populate the database by running:<br>
``
python manage.py loaddata <selected json file>
``
<br>The password for all users is ``PASSWORD!!!`` and the usernames are ``admin`` and ``user1``.
> NOTE: If using the database with the example tasks, we have written a script, populate_tests.py in the cs14-main/main directory, which will create (and remove) the necessary folders for the tasks to work.<br>
To create the necessary directories and files, run:<br>
``python populate_tests.py create_tests``<br>
To remove these, run:<br>
``python populate_tests.py remove_tests``<br>


* **Step 6** <br>
If you used one of the database dumps from **step 5**, a superuser should already be created, with the credentials:<br>
``user: admin``<br>
``password: PASSWORD!!!``<br>
If you are not using one of the database dumps, you can create a superuser with the following command:<br>
``
python manage.py createsuperuser
``

* **Step 7**<br>
Build the docker image.<br>
In the directory cs14-main/main/static/python/, run the following command:<br>
``
docker build -t coding-image .
``<br>
> Note: The docker image may take a few minutes to build, and the building process may not succeed on the first try.

* **Step 8** <br>
You can now run the site locally using the following command in the cs14-main/main/ directory:<br>
``
python manage.py runserver
``


# **ADMIN** (adding users and other objects to the database)
* Firstly, you will need to add a superuser. You should have already done this in the setup, either by using one of the provided database dumps, or by running:<br>
``python manage.py createsuperuser``<br>

* You can now log into the Django admin interface using this user. You will need to run the server first:<br>
``python manage.py runserver``<br>
Open the link that appears in the terminal, and navigate to http://127.0.0.1:8000/admin.<br>

* From here, sign in as the created superuser. You can now add values to the database.
> Note: The site admins are different to the superusers. You will have to give a superuser admin privileges so they can generate user accounts.<br>
Alternatively, you can create a new admin user. This can be done via the Django admin interface.

# **ADDING CODING TASKS**
Coding task objects are added via the Django admin interface. However, the expected output and sample input need to be added manually. To do so:

* Create a directory in cs14-main/main/media/tests/ with the name test followed by the the task id. 
For example, if the task id is 1, the folder should be named "test1", thus creating the directory cs14-main/main/media/tests/test1.

* Within this new directory, create two directories: input and output.

* In the "input" directory, create a file containing the input to the code. If no input is required, create an empty file, as **this is required for the compilation to work.**

* In the "output" directory, create a file containing the expected output of the code, which will be used for the testing.

**An example of sample input and output would be the following:**<br>

> Task description: "Write some code which takes input values from the command line and outputs their squares."<br>
<br>The input and output files should contain the following:<br>
<br>Input:<br> 
	  `1`<br>
	  `2`<br>
	  `3`<br>
	  `4`<br>
<br>Output:<br>
	  `1`<br>
	  `4`<br>
	  `9`<br>
	  `16`<br>


 

# **ADDING MORE LANGUAGES**
If you would like to add more languages, you will need to:
* Add installation instructions for the compiler/language in the Dockerfile, which can be found in cs14-main/main/static/python/
* Add code for compilation and/or running in runcontainer.py, found in cs14-main/main/static/python/
* Rebuild the Docker image
* Add the necessary file extension in the add_language_extension function found in compile.py (cs14-main/main/static/python)
* You will also need to add the required buttons in the selection menu of the coding page.
