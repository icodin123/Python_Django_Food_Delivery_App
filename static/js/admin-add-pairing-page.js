$(document).ready( function () {
    // Initialize DataTables
    var partner_table = $('#addPairingPartner').DataTable( {
        "info":false,
        "lengthChange":false,
        "pageLength":10
    } );
    var restaurant_table = $('#addPairingRestaurant').DataTable( {
        "info":false,
        "lengthChange":false,
        "pageLength":10
    } );
    var partner_chosen = false;
    var restaurant_chosen = false;
    // Make it possible to select rows from the tables
    $('#addPairingPartner').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            partner_chosen = false;
            updatePairButton();
        }
        else {
            partner_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            partner_chosen = true;
            updatePairButton();
        }
    } );
    $('#addPairingRestaurant').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            restaurant_chosen = false;
            updatePairButton();
        }
        else {
            restaurant_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            restaurant_chosen = true;
            updatePairButton();
        }
    } );
    function updatePairButton () {
        if (partner_chosen && restaurant_chosen) {
            $("#pairButton").prop('disabled', false);
        } else {
            $("#pairButton").prop('disabled', true);
        }
    }
    // Time picker code based on tempus dominus usage page
    // https://tempusdominus.github.io/bootstrap-4/Usage/
    $(function () {
        $("#timepicker").datetimepicker({
            format: 'LT'
        });
    });
} );
