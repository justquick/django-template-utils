from distutils.core import setup

setup(name='template_utils',
      version='0.4p2',
      description='Template-related utilities for Django applications',
      author='James Bennett',
      author_email='james@b-list.org',
      url='http://code.google.com/p/django-template-utils/',
      packages=['template_utils', 'template_utils.templatetags'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
