$(function() {
    $('#slider').slider({
        range: "max",
        min: 100,
        max: 1000,
        value: 600,
        step: 20,
        slide: function(event, ui) {
            $('#value').text(ui.value);
        }
    });
    $('#value').text($('#slider').slider('value'));
});