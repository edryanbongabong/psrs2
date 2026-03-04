$(document).ready(function () {
  $('.add-orderpersonnel').click(function (ev) {
    ev.preventDefault();
    var count = $('#item-orderpersonnel').children().length;
    var tmplMarkup = $('#orderpersonnel-template').html();
    var compiledTmpl = $(tmplMarkup.replace(/__prefix__/g, count));
    $('#item-orderpersonnel').append(compiledTmpl);
    compiledTmpl.find('.select2').select2({
      placeholder: "Choose from the list",
      readonly: true,
      allowClear: true,
    })
    // update form count
    $('#id_orderpersonnel-TOTAL_FORMS').attr('value', count + 1);
  });  

  $.each($('[name="message[]"]'), function(){
    Toast.fire({
      icon: $(this).data('tags'),
      title: $(this).val(),
    });
  })
});