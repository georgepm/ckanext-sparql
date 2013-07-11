var $ = jQuery.noConflict();

$('#sparql_results').hide();
$('#sparql_link_query').hide();
//$("#field-link-sparql-server-query").attr('readonly','readonly');
		
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

function call_sparql_point_server() {

    $.ajax({
		type:'GET', 
		url: 'query', 
		data: {'query' : editor.getValue(), 'server' : $("#field-sparql-server").val()}, 
		success: function(response) {
        	$('#sparql_results').html(response);
			$('#field-link-sparql-server-query').val('http://' + window.location.hostname + '/' + this.url);
			$('#sparql_results').show();
			$('#sparql_link_query').show();
    	}
		});

}