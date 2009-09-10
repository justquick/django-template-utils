from distutils.core import setup

setup(name='template_utils',
      version='0.5',
      description='Template-related utilities for Django applications',
      author='James Bennett, Justin Quick',
      author_email='james@b-list.org, justquick@gmail.com',
      url='http://github.com/justquick/django-template-utils/tree/master',
      packages=['template_utils', 'template_utils.templatetags'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
