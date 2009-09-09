=========================
Django template utilities
=========================

This is a small library of template tags and other template-related
utilities for use with Django_; while Django does a great job in
general of helping developers avoid repetitive code, there are still a
few things which tend to be useful or even needed in many different
types of projects, so this application aims to genericize and bundle
many of them into one reusable package.

.. _Django: http://www.djangoproject.com/


Downloading and installing
==========================

The easiest download method is a Subversion_ checkout; all of the code
is maintained in a Subversion repository, and checking the code out
from the repository makes it easy to handle updates. To download and
install, simply execute this command from a directory that's on your
Python path::

    svn co http://django-template-utils.googlecode.com/svn/trunk/template_utils/

This will create a directory called ``template_utils``, and download
the current code into it. From there, you should be able to add
``template_utils`` to the ``INSTALLED_APPS`` setting of any Django
project and have it work. This application provides no models, so you
don't need to run ``manage.py syncdb`` before using it.

.. _Subversion: http://subversion.tigris.org/


Using ``distutils``
-------------------

Alternatively, you can download a packaged version of the entire
application and use Python's ``distutils`` to install it::

    wget http://django-template-utils.googlecode.com/files/template_utils-0.4.tar.gz
    tar zxvf template_utils-0.4.tar.gz
    cd template_utils-0.4
    python setup.py install


Feature overview
================

Currently, five main components are bundled into ``template_utils``:

* Template tags for `generic content retrieval`_.

* Template tags for `robust comparison operations`_.

* Template tags for `retrieving public comments`_ (for when a
  comment-moderation system is in use).

* Template tags for `retrieving and parsing RSS and Atom feeds`_
  and displaying the results in template.

* A `generic text-to-HTML conversion system`_ with template filter
  support.

* A system for generating `template context processors`_ which can
  add arbitrary settings to template contexts.
  
* `Node classes`_ for simplifying some common types of custom
  template tags.
    

.. _generic content retrieval: docs/generic_content.html
.. _robust comparison operations: docs/comparison.html
.. _retrieving public comments: docs/public_comments.html
.. _retrieving and parsing RSS and Atom feeds: docs/feeds.html
.. _generic text-to-HTML conversion system: docs/markup.html
.. _template context processors: docs/context_processors.html
.. _Node classes: docs/nodes.html
