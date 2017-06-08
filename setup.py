from setuptools import setup

setup(name='falcon_oauth',
      version='0.1',
      description='Falcon OAuth Resource',
      url='https://github.com/konradbnet/falcon-oauth',
      author='Konrad Budaj',
      author_email='k@konradb.net',
      license='MIT',
      packages=['falcon_oauth'],
      install_requires=[
          'falcon',
          'requests_oauthlib',
      ],
      zip_safe=False)
