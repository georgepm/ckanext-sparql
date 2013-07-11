CKAN Sparql Interface Extension
===============================

**Status:** Production
**CKAN Version:** >= 2.*

This is a simple extension, but may be useful for someone that wants to include a Sparql Interface Editor in their CKAN instances. The idea is based on the Sparql Editor of the LODUM project from the University of Munsters Open Data initiative (http://data.uni-muenster.de/php/sparql/).

Requeriments
------------

The extension uses:

- SPARQL Endpoint interface to Python: SPARQLWrapper -> (http://sparql-wrapper.sourceforge.net/) 
- CodeMirror for the code editor in the browser -> (http://codemirror.net/)

Installation
------------

- Install SPARQL Wrapper and simplejson (Needed for the previous one) in:
  
  ckanext-sparql/ckanext/sparql/lib 

- Install the extension::
  
  $ python setup.py develop
  $ sudo service apache2 reload

