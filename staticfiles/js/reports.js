
$(document).ready(function () {

  $('#tbl_data').on('initComplete', function (event, table) {
    $('.dataTables_filter').empty()
    $('.dataTables_length').append('<a href="create/" id="create-data" class="btn btn-primary float-right" type="button"><i class="fas fa-plus"></i> Add New</a>')

    /* $("#create-data").modalForm({
      formURL: "create/"
    }); */
  });
  
  $('#tbl_data').on('draw.dt', function (table, settings) {
    $(".view-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });

    $(".delete-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, });
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

  $(document).on('click', '.submit-data', function (e) {
    var url = $(this).data('form-url');
    Confirm.fire({
      title: 'Are you sure?',
      text: 'You are about to submit a report for approval. Do you want to proceed?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Yes, submit it!',
      cancelButtonText: 'No, cancel!',
      reverseButtons: true
    }).then((result) => {
      if (result.value) {
        window.location.href = url;
      }
    });
  });

  $.each($('[name="message[]"]'), function(){
    Toast.fire({
      icon: $(this).data('tags'),
      title: $(this).val(),
    });
  })
});