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

function moveChange() {
    var size = parseInt($('input[name="size"]:checked').val());
    var C1 = parseInt($('input[name="flavor1"]').val());
    var C2 = parseInt($('input[name="flavor2"]').val());
    var C3 = parseInt($('input[name="flavor3"]').val());
    var C4 = parseInt($('input[name="flavor4"]').val());
    var totalCandy = C1 + C2 + C3 + C4;

    $('#flavor1-quan').text(C1);
    $('#flavor2-quan').text(C2);
    $('#flavor3-quan').text(C3);
    $('#flavor4-quan').text(C4);
    $('#total-quan').text(totalCandy);

    $('input[name="flavor1"]').attr('max', size-totalCandy+C1);
    $('input[name="flavor2"]').attr('max', size-totalCandy+C2);
    $('input[name="flavor3"]').attr('max', size-totalCandy+C3);
    $('input[name="flavor4"]').attr('max', size-totalCandy+C4);

    if (totalCandy < size) {
        var needMore = size - totalCandy;
        $('#alertQty').text('You need ' + needMore + ' more candies!');
    } else {
        $('#alertQty').text('Good to go!');
    }
}