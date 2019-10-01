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
          'dolmen.beaker',
          'fanstatic',
          'grok',
          'grokcore.chameleon',
          'grokcore.startup',
          'grokui.admin',
          'hurry.workflow',
          'js.jquery',
          'lxml',
          'megrok.z3ctable',
          'repoze.filesafe',
          'setuptools',
          'uvc.validation',
          'zeam.form.base',
          'zeam.form.layout',
          'zeam.form.ztk',
          'zeam.jsontemplate',
          'zope.dublincore',
          'zope.fanstatic[test]',
          'zope.location',
          'zope.pluggableauth',
          'zope.publisher',
          'zope.sendmail',
          'zope.traversing',
          'ZEO',
      ],
      entry_points={
          'fanstatic.libraries': [
              'uvcsite = uvcsite.resource:library',
          ]
      })
