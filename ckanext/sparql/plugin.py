from logging import getLogger
import ckan.plugins as p
from pylons import request, response, config
#from SPARQLWrapper import SPARQLWrapper, JSON
import urllib, json
import collections
from urlparse import urlparse
import csv

log = getLogger(__name__)

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

def sparqlQuery(data_structure):
    
    c = p.toolkit.c
    c.direct_link = request.params.get('direct_link')
    
    if request.params.get('type_response_query') == 'json': 
        format="application/json"
    elif request.params.get('type_response_query') == 'turtle':
        format="text/turtle"
    elif request.params.get('type_response_query') == 'csv':
        #The conversion to csv is made later
        format="application/json"
    elif request.params.get('type_response_query') == 'js':
        format="application/javascript"
    else:
        ## Default Format
        format="application/json"
    
    params_query={
        "default-graph": "",
        "should-sponge": "soft",
        "query": request.params.get('query'),
        "debug": "off",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": ""
    }
    
    querypart = urllib.urlencode(params_query)
    temp_result = urllib.urlopen(request.params.get('server'),querypart)
    response_query = temp_result.read()
    
    if request.params.get('type_response_query') == 'json': 
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        response.content_type = 'application/json'
        #response.headers['Content-disposition'] = 'attachment; filename=query.json'
        return json.dumps(data, separators=(',',':'))
    elif request.params.get('type_response_query') == 'turtle':
        response.content_type = 'text/turtle'
        return response_query
    elif request.params.get('type_response_query') == 'csv':
        response.content_type = 'text/plain'
        response.headers['Content-disposition'] = 'attachment; filename=query.csv'
        response.charset = "utf-8-sig"
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        output = []
        for result in data["head"]["vars"]:
            output.append(result+",")
        output.append("\n")
        
        for result in data["results"]["bindings"]:
            index = 0
            for attributes, values in result.items():
                if attributes == data["head"]["vars"][index]:
                    output.append("\"" + values['value'] + "\"" +',')
                    index += 1
                else:
                    key = 0
                    for listheader in data["head"]["vars"]:
                        if listheader != attributes and key>=index:
                            output.append(',')
                        elif listheader == attributes:
                            output.append("\"" + values['value'] + "\"" +',')
                            index = key+1
                            break
                        key += 1
            output.append("\n")
        return "".join(output)
    elif request.params.get('type_response_query') == 'js':
        response.content_type = "application/javascript"   
        return response_query
    elif request.params.get('type_response_query') == 'query':
        return "data.upf.edu/sparql?view_code=" + request.params.get('query')
    else:
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        return data

### GET FUNCTIONS ###

#Returns get/post query param data
def get_query():
    return request.params.get('query')

#Returns get/post direct_link param to check whether to return in a specific format the data
def check_direct_link():
    return request.params.get('direct_link')

#Used to check whether a string is a url
def check_is_url(strtocheck):
    results = urlparse(strtocheck)
    return results.scheme

def endpoint_url():
	endpointUrl = config.get('ckanext.sparql.endpoint_url', 'http://dbpedia.org/sparql')
	#log.debug("endpointUrl: " + endpointUrl)
	return endpointUrl

def hide_endpoint_url():
	hideEndpointUrl = p.toolkit.asbool(config.get('ckanext.sparql.hide_endpoint_url', 'False'))
	#log.debug("hideEndpointUrl: %s" % hideEndpointUrl)
	return hideEndpointUrl

### CLASS ###

class SparqlPlugin(p.SingletonPlugin):
    
    #Ckan Stuff
    
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

    ## TEMPLATE FUNCTIONS ##

    def get_helpers(self):
        return {
                'get_query': get_query, 
                'sparqlQuery': sparqlQuery, 
                'check_direct_link': check_direct_link, 
                'check_is_url': check_is_url,
                'sparql_endpoint_url': endpoint_url,
                'sparql_hide_endpoint_url': hide_endpoint_url
                #'sparql_query_SPARQLWrapper': sparql_query_SPARQLWrapper
                }
