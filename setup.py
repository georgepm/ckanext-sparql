from setuptools import setup, find_packages
import sys, os
from os import path

version = '2.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='ckanext-sparql',
	version=version,
	description="Sparql_Point",
	long_description=long_description,
    long_description_content_type="text/markdown",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Jorge Pantoja',
	author_email='jorgepantojam@gmail.com',
	url='https://github.com/OpenDataGIS/ckanext_sparql',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points="""
        [ckan.plugins]
		sparql = ckanext.sparql.plugin:SparqlPlugin
		[babel.extractors]
		ckan = ckan.lib.extract:extract_ckan
	""",

    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
