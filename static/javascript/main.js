$( document ).ready(function() {
  $('#examples a').click(function(){
    $.get(this, function( data ) {
      $('#q').val(data)
    });
    return false
  });
});
