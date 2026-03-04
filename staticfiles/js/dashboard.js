$(document).ready(function () {
  $.each($('[name="message[]"]'), function(){
    Toast.fire({
      icon: $(this).data('tags'),
      title: $(this).val(),
    });
  })
});