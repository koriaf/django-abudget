django-abudget
==============

Just another home budget application, written in Django. Allows you to start it locally or on your own server and having your data at hand at any time without sharing it to anyone.

In fact it doesn't worth it to write such application or get a separate server for it, but for if you already have the host and some time to waste...

User experience: administrator creates Categories, Budget and related stuff (example provided as fixture) and gives access to another related people.

Current status - beta. I am using it now and making improvements sometimes. It works and fullfills my needs. It seems that the project is abandoned but it's not - it just got to the state where no improvements are needed bad enough.


Code
--------

It uses Python 3.5 and currently does not require any particular database backend (works with sqlite and postgresql for my case). But given we use docker-compose it's assumed to work with Postgres. If you have some exotic hosting then it could work with other backends as well (some modifications may be required).

Js part is a little messy and just use jquery in the most stupid way, which is enough.

Installation
------------

Sometimes docker and docker-compose requires root access. You can check docker-compose.yml and Dockerfile to understand what is doing on here.

Find the `docker.env.sample` file, copy it to `docker.env` and update it (comments inside).

Then build the js libraries:

    cd src
    yarn install

And start the project:

    docker-compose up

Create some database:

    docker-compose exec web sh
    ./manage.py migrate
    ./manage.py createsuperuser

Optionally, load a fixture (to be executed inside the `web` container):

    ./manage.py loaddata fixtures/budget_and_categories_for_admin.json

It's in Russian, but helps to understand how it should be used (or doesn't, if you don't read Russian).

Wait some seconds so service `web` starts, and then navigate to the link provided.


Screenshots
-----------

![Screenshot First](https://raw.githubusercontent.com/koriaf/django-abudget/master/doc/abudget_ss_1.png)
![Screenshot Second](https://raw.githubusercontent.com/koriaf/django-abudget/master/doc/abudget_ss_2.png)
