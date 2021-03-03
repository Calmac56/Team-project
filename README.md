**Prerequisites**
- A linux distro or WSL
- An up to date install of Docker. Docker can be found here: https://www.docker.com/products/docker-desktop

**Step 1** <br>
Clone the repo using: <br>
``
git clone link
``

**Step 2** <br>
Install the requirements. <br>
CD into the cloned directory and use the following command: <br>
``
pip install -r requirements.txt
``

**Step 3** <br>
Create the database. <br>
CD into the "main" directory and run the following commands.<br>
``
python manage.py makemigrations `` <br>
``
python manage.py migrate
``

**Step 4** <br>
Populate the database. <br>
Run the following populate command <br>
``
Insert command here
``

**Step 5** <br>
Create a django admin user to manage site. <br>
Run the following terminal command <br>
``
python manage.py createsuperuser
``

**Step 6**
Run the site. <br>
Run the following terminal command <br>
``
python manage.py runserver
``

Thats it, the local version of the site should now be up and running. You can add administrator users and reviews from the django admin panel. Administrators can then generate user accounts for candidates.

