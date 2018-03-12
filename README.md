# ADVBACKEND

Three API endpoints for data statistics fetching. Implemented as django
application.

# Setup

* Create virtualenv inside project folder:
  * `virtualenv -p /usr/bin/python3 evn_advbackend`
  * `source evn_advbackend/bin/activate`
  * `pip install -r requirements.txt`

* Deactivate virtualenv:
  * `deactivate`

___

# Running

* Start the sever:
  * `./manage.py runserver`

___

# Testing

* Testing:
  * `./manage_test.py test`

___

# Data migration:

* `./manage.py makemigrations`
* `./manage.py migrate`

Data migration is time consuming process.

* Migration into inmemory sqlite db takes 320 seconds.
* Migration into local sqlite db takes 341 seconds.

___
