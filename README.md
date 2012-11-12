KiUR
=============

About
-----
KiUR is the KiCAD User Repository. It is a site to share KiCAD schematic symbol and footprint libraries.

The planned features are:

* easy upload, batch upload and versioning of libraries
* suggested footprints for schematic symbols
* vote on inclusion into the standard libraries
* comment and flag problems with libraries
* search, download and batch download for easy library management

Deploying Your own Development Site
-----------------------------------

* install the dependencies listed below
* run database software and set up a database for KiUR to use
* put the database and a secret key (you can just make it up) into a file kiur/secrets.py in the normal settings.py format
* run ./manage.py runserver


Dependencies
------------

* Python 2.7
* MySQL (or another database)

From PyPI:

* django
* mysql-python (or another database interface)
* easy-thumbnails
* PIL
* django-haystack
* whoosh

