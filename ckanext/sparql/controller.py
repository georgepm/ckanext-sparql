import ckan.plugins as p
from ckan.lib.base import BaseController, render, config
import ckan.lib.helpers as h

class SparqlController(BaseController):

    def index(self):
        return render('ckanext/sparql/index.html')

    def query_page(self):
        return render('ckanext/sparql/query.html');
