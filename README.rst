django-abudget
==============
Just another home budget application, written in Django. Just because I haven't found something perfectly fit. And I definetly don't like then someone have all my finance information, so, this project is being written for people like me, who can manage to start it on local server for personal use. Or ask someone who can :-)

Assuming that you will have admin access and create some objects (IncomeCategory, TransactionCategory, Budget) from admin panel, and then add some users to share budgets.

Current status - pre-alpha. I am using it and improve sometimes.


| |Build Status|

Code
--------

It uses Python 3.4 and currently does not require any particular database backend.

I am going to make a lot of ajax stuff here, so - no form error display, and some things also done quick way, not right way. I will replace it to completely different code anyway, when time comes.

Going to use react to handle client-side data processing logic, but jquery nice for now.

Going to make install and other instruction later.

Installing
----------

(from memory, haven't tested these commands)

source ./venv.sh
pip install -r system/requirements.prod.txt
psql
   create database abudget;
   create role abudget with password 'wow' login;
   grant all privileges on database abudget to abudget;
cd src/abudget/settings/
cp prod.py.sample prod.py
vim prod.py
cd ../..
./manage.sh migrate
./manage.sh createsuperuser
(optional) ./manage.sh loaddata fixtures/budget_and_categories_for_admin.json

...

Testing
----------
./test-dev.sh (after venv install)

...

Deployment
----------

Use https!

...


Screenshots
-----------

.. image:: https://raw.githubusercontent.com/koriaf/django-abudget/master/abudget_ss_1.png

.. image:: https://raw.githubusercontent.com/koriaf/django-abudget/master/abudget_ss_2.png


.. |Build Status| image:: https://travis-ci.org/koriaf/django-abudget.svg?branch=master
   :target: https://travis-ci.org/koriaf/django-abudget
