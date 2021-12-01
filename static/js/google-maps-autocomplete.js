$(document).ready( function () {
    var input = document.getElementById('address');

    var options = {
        fields: ['address_component', 'geometry'],
        location: '43.717899,-79.6582408'
    };

    autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.setComponentRestrictions({'country': ["CA"]});
    autocomplete.addListener('place_changed', function() {
        // Update coordinates whenever a place is selected
        var place = autocomplete.getPlace();
        $('#lat').val(place.geometry.location.lat());
        $('#lng').val(place.geometry.location.lng());
    });



} );
