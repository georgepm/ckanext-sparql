from urllib.parse import urlparse
import ckan.plugins as p
from ckanext.sparql.utils import sparqlQuery as utils_sparqlQuery
from logging import getLogger


logger = getLogger(__name__)

all_helpers = {}

def helper(fn):
    """
    collect helper functions into ckanext.sparql.all_helpers dict
    """
    all_helpers[fn.__name__] = fn
    return fn

### GET FUNCTIONS ###

#Returns get/post query param data

@helper
def get_query():
    return p.toolkit.request.params.get('query')

#Returns get/post direct_link param to check whether to return in a specific format the data

@helper
def check_direct_link():
    return p.toolkit.request.params.get('direct_link')

#Used to check whether a string is a url

@helper
def check_is_url(strtocheck):
    results = urlparse(strtocheck)
    return results.scheme

@helper
def sparql_endpoint_url():
    endpointUrl = p.toolkit.config.get('ckanext.sparql.endpoint_url', 'http://dbpedia.org/sparql')
    #logger.debug("endpointUrl: " + endpointUrl)
    return endpointUrl

@helper
def sparql_hide_endpoint_url():
    hideEndpointUrl = p.toolkit.asbool(p.toolkit.config.get('ckanext.sparql.hide_endpoint_url', 'False'))
    #logger.debug("hideEndpointUrl: %s" % hideEndpointUrl)
    return hideEndpointUrl

@helper
def sparqlQuery(data_structure):
    return utils_sparqlQuery(data_structure)