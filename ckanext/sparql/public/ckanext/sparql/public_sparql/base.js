var $ = jQuery.noConflict();

$('#sparql_results').hide();
$('#sparql_link_query').hide();
$('#loading_image').hide();
		
// The CodeMirror stuff
var editor = CodeMirror.fromTextArea(document.getElementById("sparql_code"), {
  mode: "application/x-sparql-query",
  lineNumbers: true,
  onCursorActivity: function() {
    editor.setLineClass(hlLine, null);
    hlLine = editor.setLineClass(editor.getCursor().line, "activeline");
  }
});

var hlLine = editor.setLineClass(0, "activeline");

var prefixes = "PREFIX void: <http://rdfs.org/ns/void#> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX vann: <http://purl.org/vocab/vann/> PREFIX teach: <http://linkedscience.org/teach/ns#> PREFIX dcterms: <http://purl.org/dc/terms/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX dcat: <http://www.w3.org/ns/dcat#> PREFIX crsw: <http://courseware.rkbexplorer.com/ontologies/courseware#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#> PREFIX univcat: <http://data.upf.edu/upf/ontologies/universidadcatalana#> PREFIX skos: <http://www.w3.org/2004/02/skos/core#> PREFIX vivo: <http://vivoweb.org/ontology/core#> PREFIX sbench: <http://swat.cse.lehigh.edu/onto/univ-bench.owl#> PREFIX sdmx-attribute: <http://purl.org/linked-data/sdmx/2009/attribute#> PREFIX sdmx-concept: <http://purl.org/linked-data/sdmx/2009/concept#> PREFIX sdmx-code: <http://purl.org/linked-data/sdmx/2009/code#> PREFIX disco: <http://rdf-vocabulary.ddialliance.org/discovery#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX sdmx-measure: <http://purl.org/linked-data/sdmx/2009/measure#> PREFIX qb: <http://purl.org/linked-data/cube#> PREFIX sdmx: <http://purl.org/linked-data/sdmx#>"

function call_sparql_point_server() {
	
	//Controls
	
	if ($("#field-sparql-server").val().length == 0) {
        $('#loading_image').hide();
        $('#sparql_results').show();
        $('#sparql_results').html("<div class='alert alert-error'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error: </strong>Please add the Sparql Point Server URL. For Instance: http://semantic.ckan.net/sparql. </div>");
        return;
    }
	
	//Jquery Stuff
	
	$('#sparql_results').html("");
	$('#go_to_link_query').attr("href", '');
	$('#field-link-sparql-server-query').val('');
	$('#sparql_link_query').hide();
	$('#sparql_results').hide();
	$('#loading_image').show();
	
    $.ajax({
		type:'GET', 
		url: 'query', 
		data: {'query' : prefixes + get_sparql_string(), 'server' : $("#field-sparql-server").val(), 'direct_link': 0}, 
		success: function(response) {
        	$('#sparql_results').html(response);
        	        	
        	base_address=queryHref()+ '/' + change_direct_link_value(this.url)
        	
			$('#field-link-sparql-server-query_json').val(base_address + add_extra_fields_url('json'));
			$('#go_to_link_query_json').attr("href", base_address + add_extra_fields_url('json'));
			
			$('#field-link-sparql-server-query_turtle').val(base_address + add_extra_fields_url('turtle'));
			$('#go_to_link_query_turtle').attr("href", base_address + add_extra_fields_url('turtle'));
			
			$('#field-link-sparql-server-query_csv').val(base_address + add_extra_fields_url('csv'));
			$('#go_to_link_query_csv').attr("href", base_address + add_extra_fields_url('csv'));
			
			console.log("base_address: %s",base_address)
			console.log("")
			
			//$('#go_to_link_query_query').attr("href", 'http://' + window.location.hostname + '/en/sparql?' + $.param({'view_code' : prefixes + editor.getValue()}));
			$('#go_to_link_query_query').attr("href", window.location.pathname + '?' + $.param({'view_code' : prefixes + editor.getValue()}));
			
			$('#sparql_results').show();
			$('#sparql_link_query').show();
			$('#loading_image').hide();
    	},
    	error: function (request, status, error) {
	        $('#loading_image').hide();
	        $('#sparql_results').show();
	        $('#sparql_results').html("<div class='alert alert-error'><a href='#' class='close' data-dismiss='alert'>&times;</a><strong>Error: </strong>Please Verify your query. </div>");
        	return;
	    }
		});

}

function change_direct_link_value(url) {
	console.log("url:"+url)
	var new_url = url.substring(0, url.length-1);
	return new_url + '1';
}

function add_extra_fields_url(field) {
	if (field == 'json')
		var sparql_extra_fields = '&type_response_query=json';
	else if (field == 'turtle')
		var sparql_extra_fields = '&type_response_query=turtle';
	else if (field == 'csv')
		var sparql_extra_fields = '&type_response_query=csv';
	else
		var sparql_extra_fields = '';
	return sparql_extra_fields;
}

function view_resource(resource) {
   
   var hash_mark = resource.split("#")[1];
   var form = $('<form target="_blank" action="' + resource + '" method="post">' +
				'<input type="hidden" name="param_query" value="' + hash_mark + '" />' +
	  			'</form>');
   $('body').append(form);
   $(form).submit();
   
}

function GetURLParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) 
        {
            return sParameterName[1];
        }
    }
}

function get_sparql_string() {
	var sparql_string = editor.getValue();
	var unicode_string = toUnicode(sparql_string);
	//$('#test_sparql').text(unicode_string);
	return unicode_string;
}

//Author: http://buildingonmud.blogspot.com.es/2009/06/convert-string-to-unicode-in-javascript.html
//Only for TextArea
function toUnicode(theString) {
  var unicodeString = '';
  var regex = new RegExp(/[^\w\s\n\t`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/g);
  for(var j=0; j < theString.length; j++) {
    if(theString.charAt(j).match(regex)) {
	    var theUnicode = theString.charCodeAt(j).toString(16).toUpperCase();
	    while (theUnicode.length < 4) {
	      theUnicode = '0' + theUnicode;
	    }
	    theUnicode = '\\u' + theUnicode;
	    unicodeString += theUnicode;
    } else {
    	unicodeString += theString.charAt(j);
    }
  }
  return unicodeString;
}

function queryHref() {
	respuesta=window.location.origin;
	steps=window.location.pathname.split("/");
	for (var i=1; i < (steps.length-1); i++) {
		respuesta+="/"+steps[i];
	}
	return respuesta;
}