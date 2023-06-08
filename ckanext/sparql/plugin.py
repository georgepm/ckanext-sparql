import collections
import json
import urllib
from logging import getLogger
from urllib.parse import urlparse
from urllib.request import urlopen

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from flask import Blueprint

log = getLogger(__name__)

### SPARQL QUERY FUNCTIONS ###

## OPTIONAL: NOT USED ##
"""def sparql_query_SPARQLWrapper(data_structure):
    c = p.toolkit.c
    queryString = tk.request.params.get('query')
    sparql = SPARQLWrapper(tk.request.params.get('server'))
    sparql.setQuery(queryString)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    c.sparql_query = queryString
    return results
"""


def sparqlQuery(data_structure):
    type_response_query = tk.request.params.get("type_response_query")

    c = p.toolkit.c
    c.direct_link = tk.request.params.get("direct_link")

    if type_response_query == "json":
        format = "application/json"
    elif type_response_query == "turtle":
        format = "text/turtle"
    elif type_response_query == "csv":
        # The conversion to csv is made later
        format = "application/json"
    elif type_response_query == "js":
        format = "application/javascript"
    else:
        ## Default Format
        format = "application/json"

    params_query = {
        "default-graph": "",
        "should-sponge": "soft",
        "query": tk.request.params.get("query"),
        "debug": "off",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": "",
    }

    querypart = urllib.urlencode(params_query)
    log.debug("querypart: " + querypart)

    server = tk.request.params.get("server")
    log.debug("server: " + server)

    temp_result = urlopen(server, querypart)
    response_query = temp_result.read()
    log.debug("response_query: " + response_query)

    if type_response_query == "json":
        data = json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        return json.dumps(data, separators=(",", ":"))
    elif type_response_query == "turtle":
        return response_query
    elif type_response_query == "csv":
        data = json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        output = []
        for result in data["head"]["vars"]:
            output.append(result + ",")
        output.append("\n")

        for result in data["results"]["bindings"]:
            index = 0
            for attributes, values in result.items():
                if attributes == data["head"]["vars"][index]:
                    output.append('"' + values["value"] + '"' + ",")
                    index += 1
                else:
                    key = 0
                    for listheader in data["head"]["vars"]:
                        if listheader != attributes and key >= index:
                            output.append(",")
                        elif listheader == attributes:
                            output.append('"' + values["value"] + '"' + ",")
                            index = key + 1
                            break
                        key += 1
            output.append("\n")
        return "".join(output)
    elif type_response_query == "js":
        return response_query
    elif type_response_query == "query":
        return "data.upf.edu/sparql?view_code=" + tk.request.params.get("query")
    else:
        data = json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        return data


### GET FUNCTIONS ###

# Returns get/post query param data
def get_query():
    return tk.request.params.get("query")


# Returns get/post direct_link param to check whether to return in a specific format the data
def check_direct_link():
    return tk.request.params.get("direct_link")


# Used to check whether a string is a url
def check_is_url(strtocheck):
    results = urlparse(strtocheck)
    return results.scheme


def endpoint_url():
    endpointUrl = tk.config.get(
        "ckanext.sparql.endpoint_url", "http://dbpedia.org/sparql"
    )
    # log.debug("endpointUrl: " + endpointUrl)
    return endpointUrl


def hide_endpoint_url():
    hideEndpointUrl = p.toolkit.asbool(
        tk.config.get("ckanext.sparql.hide_endpoint_url", "False")
    )
    # log.debug("hideEndpointUrl: %s" % hideEndpointUrl)
    return hideEndpointUrl


### CONTROLERS ###


def index():
    return tk.render("ckanext/sparql/index.html")


def query_page():
    return tk.render("ckanext/sparql/query.html")


### CLASS ###


class SparqlPlugin(p.SingletonPlugin):

    # Ckan Stuff

    """Sparql plugin."""

    p.implements(p.IBlueprint, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    def get_blueprint(self):
        blueprint = Blueprint("foo", self.__module__)
        blueprint.add_url_rule("/sparql", "sparql", index)
        blueprint.add_url_rule("/query", "sparql_query", query_page)
        return blueprint

    def update_config(self, config):
        p.toolkit.add_template_directory(config, "templates")
        p.toolkit.add_public_directory(config, "public/ckanext/sparql")
        p.toolkit.add_resource("public/ckanext/sparql", "ckanext_sparql")

    ## TEMPLATE FUNCTIONS ##

    def get_helpers(self):
        return {
            "get_query": get_query,
            "sparqlQuery": sparqlQuery,
            "check_direct_link": check_direct_link,
            "check_is_url": check_is_url,
            "sparql_endpoint_url": endpoint_url,
            "sparql_hide_endpoint_url": hide_endpoint_url,
        }
