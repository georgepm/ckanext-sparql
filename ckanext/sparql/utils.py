import ckan.plugins as p
import collections
import urllib
from logging import getLogger
from ckan.common import json
from flask import make_response

logger = getLogger(__name__)

def sparqlQuery(data_structure):
    logger.debug("Entering sparqlQuery")
    c = p.toolkit.c
    c.direct_link = p.toolkit.request.params.get('direct_link')
    
    if p.toolkit.request.params.get('type_response_query') == 'json': 
        format="application/json"
    elif p.toolkit.request.params.get('type_response_query') == 'turtle':
        format="text/turtle"
    elif p.toolkit.request.params.get('type_response_query') == 'csv':
        #The conversion to csv is made later
        format="application/json"
    elif p.toolkit.request.params.get('type_response_query') == 'js':
        format="application/javascript"
    else:
        ## Default Format
        format="application/json"
    logger.debug("Format: "+format)
    params_query={
        "default-graph": "",
        "should-sponge": "soft",
        "query": p.toolkit.request.params.get('query'),
        "debug": "off",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": ""
    }
    
    querypart = urllib.parse.urlencode(params_query)
    logger.debug("querypart: " + querypart)

    server = p.toolkit.request.params.get('server')
    logger.debug("server: " + server)

    logger.debug("url: {0}?{1}".format(server, querypart))


    temp_result = urllib.request.urlopen("{0}?{1}".format(server, querypart))
    temp_response_query = temp_result.read()
    response_query = temp_response_query.decode("utf-8")
    logger.debug("response_query: {}".format(response_query))

    if p.toolkit.request.params.get('type_response_query') == 'json': 
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        response = make_response(json.dumps(data, separators=(',',':')))
        response.content_type = 'application/json'
        #response.headers['Content-disposition'] = 'attachment; filename=query.json'
        return response
        #logger.debug("data: {}".format(data))
        #return data
    elif p.toolkit.request.params.get('type_response_query') == 'turtle':
        response = make_response(response_query)
        response.content_type = 'text/turtle'
        return response
    elif p.toolkit.request.params.get('type_response_query') == 'csv':
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
        response = make_response("".join(output))
        response.content_type = 'text/csv'
        #p.toolkit.response.headers['Content-disposition'] = 'attachment; filename=query.csv'
        response.charset = "utf-8-sig"
        return response
    elif p.toolkit.request.params.get('type_response_query') == 'js':
        p.toolkit.response.content_type = "application/javascript"   
        return response_query
    elif p.toolkit.request.params.get('type_response_query') == 'query':
        return "data.upf.edu/sparql?view_code=" + p.toolkit.request.params.get('query')
    else:
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        return data

def sparqlQueryold(data_structure):
    
    c = p.toolkit.c
    c.direct_link = p.toolkit.request.params.get('direct_link')
    
    if p.toolkit.request.params.get('type_response_query') == 'json': 
        format="application/json"
    elif p.toolkit.request.params.get('type_response_query') == 'turtle':
        format="text/turtle"
    elif p.toolkit.request.params.get('type_response_query') == 'csv':
        #The conversion to csv is made later
        format="application/json"
    elif p.toolkit.request.params.get('type_response_query') == 'js':
        format="application/javascript"
    else:
        ## Default Format
        format="application/json"
    
    params_query={
        "default-graph": "",
        "should-sponge": "soft",
        "query": p.toolkit.request.params.get('query'),
        "debug": "off",
        "timeout": "",
        "format": format,
        "save": "display",
        "fname": ""
    }
    
    querypart = urllib.urlencode(params_query)
    logger.debug("querypart: " + querypart)

    server = p.toolkit.request.params.get('server')
    logger.debug("server: " + server)

    temp_result = urllib2.urlopen(server, querypart)
    response_query = temp_result.read()
    logger.debug("response_query: " + response_query)
    
    if p.toolkit.request.params.get('type_response_query') == 'json': 
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        p.toolkit.response.content_type = 'application/json'
        #response.headers['Content-disposition'] = 'attachment; filename=query.json'
        return json.dumps(data, separators=(',',':'))
    elif p.toolkit.request.params.get('type_response_query') == 'turtle':
        p.toolkit.response.content_type = 'text/turtle'
        return response_query
    elif p.toolkit.request.params.get('type_response_query') == 'csv':
        p.toolkit.response.content_type = 'text/plain'
        p.toolkit.response.headers['Content-disposition'] = 'attachment; filename=query.csv'
        p.toolkit.response.charset = "utf-8-sig"
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
    elif p.toolkit.request.params.get('type_response_query') == 'js':
        p.toolkit.response.content_type = "application/javascript"   
        return response_query
    elif p.toolkit.request.params.get('type_response_query') == 'query':
        return "data.upf.edu/sparql?view_code=" + p.toolkit.request.params.get('query')
    else:
        data=json.loads(response_query, object_pairs_hook=collections.OrderedDict)
        return data
