Django template utilities
=========================

This is a small library of template tags and other template-related
utilities for use with Django. They are designed to be an alternative to
actually writing new templatetags, instead it offers register/unregister
functionality that lets you define functions to handle the tag at any point
in your code base. Of course it requires [Django](http://www.djangoproject.com/)


Downloading and installing
==========================

The easiest download method is a Git clone. All of the code
is maintained in a Git repository, and checking the code out
from the repository makes it easy to handle updates and contributions.
To download and install, simply clone the project from github

    $ git clone git://github.com/justquick/django-template-utils.git  

This will create a directory called ``template_utils``, and download
the current code into it. From there, you should be able to add
``template_utils`` to your ``INSTALLED_APPS`` setting of any Django
project and have it work. This application provides no models, so you
don't need to run ``manage.py syncdb`` before using it.


Using ``distutils``
-------------------

Alternatively, you can download a packaged version of the entire
application and use Python's ``distutils`` to install it::

    wget -O template_utils.tar.gz http://github.com/justquick/django-template-utils/tarball/master
    tar zxvf template_utils.tar.gz
    cd justquick-django-template-utils-......... (this is unique for each release, tab completion is your friend)
    sudo python setup.py install


Feature overview
================

Currently, five main components are bundled into ``template_utils``:

* Template tags for `generic content retrieval`. See docs/generic_content.txt

* Template tags for `robust, custom comparison operations`. See docs/comparison.txt

* Template tags for `retrieving public comments`_ (for when a
  comment-moderation system is in use). See docs/public_comments.txt

* Template tags for `retrieving and parsing RSS and Atom feeds`_
  and displaying the results in template. See docs/feeds.txt

* A `generic text-to-HTML conversion system`_ with template filter
  support. See docs/markup.txt

* A system for generating `template context processors`_ which can
  add arbitrary settings to template contexts. See docs/context_processors.txt
  
* `Node classes`_ for simplifying some common types of custom
  template tags. See docs/nodes.txt
    
