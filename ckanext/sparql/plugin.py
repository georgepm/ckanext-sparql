import ckanext.sparql.helpers as sparql_helpers
from logging import getLogger
from ckanext.sparql import blueprint
from ckan.lib.plugins import DefaultTranslation
import ckan.plugins as p
#from SPARQLWrapper import SPARQLWrapper, JSON
import collections
import csv

logger = getLogger(__name__)

### SPARQL QUERY FUNCTIONS ###

## OPTIONAL: NOT USED ##
'''def sparql_query_SPARQLWrapper(data_structure):
    c = p.toolkit.c
    queryString = request.params.get('query')
    sparql = SPARQLWrapper(request.params.get('server'))
    sparql.setQuery(queryString)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    c.sparql_query = queryString
    return results
'''


### CLASS ###

class SparqlPlugin(p.SingletonPlugin, DefaultTranslation):
    
    #Ckan Stuff
    
    '''Sparql plugin.'''

    p.implements(p.IBlueprint)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.ITranslation)

    def get_blueprint(self):
        return blueprint.sparql

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public/ckanext/sparql')
        p.toolkit.add_resource('public/ckanext/sparql', 'ckanext_sparql')

    ## TEMPLATE FUNCTIONS ##

    def get_helpers(self):
        logger.debug('Getting helpers...')
        respuesta=dict(sparql_helpers.all_helpers)
        return respuesta
