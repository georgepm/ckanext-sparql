# encoding: utf-8

from flask import Blueprint

from ckan.plugins.toolkit import c, render, request
import ckan.lib.helpers as h
from ckanext.sparql.utils import sparqlQuery as utils_sparqlQuery


sparql = Blueprint(u'sparql', __name__)


@sparql.route(u'/sparql')
def index():
    return render('ckanext/sparql/index.html')

@sparql.route(u'/query')
def query_page():
    if request.params.get('direct_link')=='0':
        return render('ckanext/sparql/query.html')
    else:
        return utils_sparqlQuery('')
