$(document).ready( function() {
  $('#vdc_table').dataTable( {
    "aoColumnDefs": [ { "bSortable": false, "aTargets": [ 6 ], } ],
    "bFilter": false, 
    "bInfo": false,
    "bPaginate": false,
	} );
} );

//For VDC Admin Page, create modal functionality
$("*[id*=vdc_update_link]:visible").each(
    function() { 
        $(this).click(
            function(e){
                e.preventDefault();
                $("#modal").load(this.href, function(){$("#modal").modal("show");
        });
    });
});