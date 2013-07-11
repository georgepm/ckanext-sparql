from logging import getLogger
import ckan.plugins as p
from pylons import request
from SPARQLWrapper import SPARQLWrapper, JSON

log = getLogger(__name__)

def sparql_query():
    c = p.toolkit.c
    queryString = request.params.get('query')
    sparql = SPARQLWrapper(request.params.get('server'))
    sparql.setQuery(queryString)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    c.sparql_query = queryString
    return results

def get_query():
    return request.params.get('query')

class SparqlPlugin(p.SingletonPlugin):
    '''Sparql plugin.'''

    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    def after_map(self, map):
        map.connect('sparql', '/sparql',
            controller='ckanext.sparql.controller:SparqlController',
            action='index')
        map.connect('sparql_query', '/query',
            controller='ckanext.sparql.controller:SparqlController',
            action='query_page')
        return map

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public/ckanext/sparql')
        p.toolkit.add_resource('public/ckanext/sparql', 'ckanext_sparql')

    def get_helpers(self):
        return {'sparql_query': sparql_query, 'get_query': get_query}
