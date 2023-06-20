# CKAN Sparql Interface Extension

Note: The ``ckanext-sparql`` extension was tested using ``Virtuoso sparql instances`` such as http://semantic.ckan.net/sparql.

I will try to make it work for other type of sparql instances ;)

- **Version:** 2.0
- **Status:** Development
- **CKAN Version:** >= 2.9

##Description

This is a simple extension, but may be useful for someone that wants to include a Sparql Interface Editor in their CKAN instances. The idea is based on the Sparql Editor of the LODUM project from the University of Munsters Open Data initiative (http://data.uni-muenster.de/php/sparql/).

##Requeriments


The extension use:

- ``CodeMirror`` for the code editor in the browser -> (http://codemirror.net/)

May be extended to use ``SPARQLWrapper`` (http://sparql-wrapper.sourceforge.net/) library - SPARQL Endpoint interface to Python

##Installation

To install ckanext-iepnb:

1. Activate your CKAN virtual environment, for example:

     `. /usr/lib/ckan/default/bin/activate`

2. Clone the source and install it on the virtualenv

    ```
    git clone https://github.com/OpenDataGIS/ckanext-sparql.git
    cd ckanext-sparql
    pip install -e .
	pip install -r requirements.txt
    ```

3. Add `sparql` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).
   
4. In order to let the English profile work, is absolutely mandatory to make the directory 
   `/ckan/ckan/public/base/i18n` writable by the ckan user. ¡CKAN WILL NOT START IF
   YOU DON'T DO SO!
   
5. Add iepnb specific configuration to the CKAN config file (see below)
   
6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     `sudo service apache2 reload`
  
##USE


Go to:
::
	http://[Custom URL]/sparql

Querys work in:
::
	http://[Custom URL]/query?query=

To send code through ``http`` to the sparql interface:
::
	http://[Custom URL]/sparql?view_code=

##CONFIGURATION

In your ``ckan.ini`` file set 
```ini
	ckanext.sparql.endpoint_url = <your default endpoint url>    (defaults to http://dbpedia.org/sparql)
	ckanext.sparql.hide_endpoint_url = (true | false)    (defaults to false)
```
  
##Notes

To configure your own custom example query 
```
	Line 54, After
	<textarea id="sparql_code" name="sparql_code"  resize="both">
	Here replace the query
	...
	</textarea>
```
  
##Changelog

- Version: 1.01: Fix Bugs 
- Version: 2.0: Adapted to ckan 2.9 and internacionalized

Example
=======

- http://data.upf.edu/sparql


ToDos
=====

* externalize configuration of default query
