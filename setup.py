from setuptools import setup, find_packages
import os

version = '1.0.2'

setup(name='jyu.datautils',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='tojuhaka',
      author_email='tojuhaka@gmail.com',
      url='http://jyuplone.cc.jyu.fi/hg/jyu.datautils',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['jyu'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'five.grok',
          'Products.CMFPlone',
          # -*- Extra requirements: -*-
      ],
      extras_require = {
          'test': ['plone.app.testing',]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      # -*- Entry points: -*-
      """,
      )
