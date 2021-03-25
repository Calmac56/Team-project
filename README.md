**Prerequisites**
- A linux distro or WSL2
- An up to date install of Docker. Docker can be found here: https://www.docker.com/products/docker-desktop
- A version of python installed that is between 3.5 and 3.9

**Step 1** <br>
Clone the repo using: <br>
``
git clone link
``
**Step 2** <br>
Run the setup script in the cs14-main folder: <br>
``
python setup.py
``
If you do this, you can skip to **Step 8**.
Alternatively, (or if this script fails), do the following steps.<br>

**Step 3** <br>
Install the requirements. <br>
CD into the cloned directory and use the following command: <br>
``
pip install -r requirements.txt
``

**Step 4** <br>
Create the database. <br>
CD into the "main" directory and run the following commands.<br>
``
python manage.py makemigrations `` <br>
``
python manage.py makemigrations cs14 `` <br>

``
python manage.py migrate
``

**Step 5** <br>
Populate the database. <br>
Run the following populate command <br>
``
python manage.py loaddata db.json
``

**Step 6** <br>
Create a django admin user to manage site. <br>
Run the following terminal command <br>
``
python manage.py createsuperuser
``

**Step 7**<br>
Setup the docker image.<br>
Run the following terminal command <br>
``
python setup.py
``<br>
Note: The docker image may take a few minutes to compile

**Step 8** <br>
Run the site. <br>
Run the following terminal command <br>
``
python manage.py runserver
``

Thats it, the local version of the site should now be up and running. You can add administrator users and reviews from the django admin panel. Administrators can then generate user accounts for candidates.

