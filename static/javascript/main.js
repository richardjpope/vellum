$( document ).ready(function() {

  //examples
  $('#examples a').click(function(){
    $.get(this, function( data ) {
      $('#q').val(data)
    });
    return false
  });

  //read
  $('.read').click(function(){
      $('#fulltext').modal();
      highlighted = $('#fulltext .modal-body').text()
      highlighted = highlighted.replace($(this).text(), '<strong id="highlighted">' + $(this).text() + '</strong>');
      $('#fulltext .modal-body').html(highlighted);
  });

  $('#fulltext').on('shown.bs.modal', function (e) {
    $('#fulltext .modal-content').css({top:'-' + Math.floor($('#highlighted').position().top) + 'px'})
  })

});
