from setuptools import setup, find_packages

version = '0.0'

setup(name='uvcsite',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[],
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'fanstatic',
          'grok',
          'grokcore.chameleon',
          'grokcore.startup',
          'grokui.admin',
          'setuptools',
          'zeam.form.base',
          'zeam.form.ztk',
          'zope.dublincore',
          'zope.fanstatic[test]',
          'zope.location',
          'zope.pluggableauth',
          'zope.publisher',
          'zope.traversing',
          'js.jquery',
          'zeam.jsontemplate',
      ],
      entry_points={
          'fanstatic.libraries': [
              'uvcsite = uvcsite.resource:library',
          ]
      })
