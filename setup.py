from setuptools import setup

setup(name='biggmodeldata',
      version='0.1',
      description='Collection of scripts for working with BIGG model data.',
      url='TBD',
      author='Stanislav Sokolenko',
      author_email='stanislav@sokolenko.net',
      license='Apache-2.0',
      packages=['biggmodeldata'],
      package_data={'biggmodeldata':['data/*']},
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      install_requires=[
          'lxml',
          'peewee',
          'requests',
      ],)
