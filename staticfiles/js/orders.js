$(document).ready(function () {

  $('#tbl_data').on('initComplete', function (event, table) {
    $('.dataTables_filter').empty()
    $('.dataTables_length').append('<a href="create/" id="create-data" class="btn btn-primary float-right" type="button">Add New</a>')

    // $("#create-data").modalForm({
    //   formURL: "create/"
    // });
  });
  
  $('#tbl_data').on('draw.dt', function (table, settings) {
    // $(".update-data").each(function () {
    //   $(this).modalForm({ formURL: $(this).data("form-url") });
    // });

    $(".delete-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, modalID: "#modal-sm" });
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