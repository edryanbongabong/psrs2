
$(document).ready(function () {

  $('#tbl_data').on('initComplete', function (event, table) {
    $('.dataTables_filter').empty()
  });
  
  $('#tbl_data').on('draw.dt', function (table, settings) {
    $(".view-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });
  });

  AjaxDatatableViewUtils.initialize_table(
    $('#tbl_data'),
    "all/",
    {
      processing: false,
      autoWidth: false,
      full_row_select: false,
      scrollX: false
    }, {},
  );

  $.each($('[name="message[]"]'), function(){
    Toast.fire({
      icon: $(this).data('tags'),
      title: $(this).val(),
    });
  })
});