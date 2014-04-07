from setuptools import setup, find_packages

setup(name='collective.classifiers',
      version='0.4.2.dev0',
      description="Themes and categories behavior",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
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
