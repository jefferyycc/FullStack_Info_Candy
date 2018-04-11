// add something if we need some interaction in javascript.
  // var elem = document.querySelector('select');
  // var instance = M.FormSelect.init(elem, options);

  // Or with jQuery

  $(document).ready(function(){

  $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
  });

  setInterval(function(){
  	$('.carousel.carousel-slider').carousel('next');
  },2000)
  });

  $(document).ready(function(){
    var elem = document.querySelector('.fixed-action-btn');
  	var instance = M.FloatingActionButton.init(elem, {
    direction: 'left',
    hoverEnabled: false
  });
  });
  
  $(document).ready(function(){
    $('.parallax').parallax();
  });

   $(document).ready(function(){
    $('select').formSelect();
  });