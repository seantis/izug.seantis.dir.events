from setuptools import setup, find_packages
import os

version = '1.2b'  # aligned with seantis.dir.base

setup(name='izug.seantis.dir.events',
      version=version,
      description="Integration of seantis.dir.events into izug",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Seantis GmbH',
      author_email='info@seantis.ch',
      url='https://github.com/seantis/izug.seantis.dir.events',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['izug', 'izug.seantis', 'izug.seantis.dir'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'seantis.dir.events',
          'izug.basetheme',
          'collective.geo.zugmap',
          'plone.app.theming'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
