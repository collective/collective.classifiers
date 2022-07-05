from setuptools import setup, find_packages

setup(name='collective.classifiers',
      version='1.0.0b2',
      description="Themes and categories behavior",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from https://pypi.org/classifiers/
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Framework :: Plone",
          "Framework :: Plone :: 5.2",
          "Framework :: Plone :: 6.0",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          ],
      keywords='collective.classifiers theme info class',
      author='Zest Software',
      author_email='info@zestsoftware.nl',
      url='http://zestsoftware.nl/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
          'plone.behavior',
          'zope.component',
          'zope.interface',
          'zope.schema',
      ],
      extras_require = {
          'test': [
              'plone.app.dexterity',
              'plone.app.testing',
              ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
