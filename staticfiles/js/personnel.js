
function changeProfile(val, frm){
  switch (val) {
    case "CHR":
      frm.find('[name="afpsn"]').prop('required', false).prop('readonly', true)
      frm.find('[name="afpsn"]').closest('.form-group').find('label').removeClass('required')
      frm.find('[name="item_no"]').prop('required', true).prop('readonly', false)
      frm.find('[name="item_no"]').closest('.form-group').find('label').addClass('required')
      frm.find('[name="rank"] option[value]:not([data-type=CHR])').prop('disabled', true)
      frm.find('[name="bos"] option[value]:not([data-ms=CHR])').prop('disabled', true)
      frm.find('[name="first_name"]').removeClass('text-uppercase')
      frm.find('[name="middle_name"]').removeClass('text-uppercase')
      frm.find('[name="last_name"]').removeClass('text-uppercase')
      frm.find('[name="ext_name"]').removeClass('text-uppercase')
      frm.find('[name="position"]').prop('disabled', false)
      frm.find('[name="fos"]').val('').prop('disabled', true)
      frm.find('[name="daghq"]').val('').prop('disabled', true)
      frm.find('[name="dapda"]').val('').prop('disabled', true)
      frm.find('[name="rrfcd"]').val('').prop('disabled', true)
      frm.find('[name="skills"]').val('').prop('disabled', true)
      frm.find('[name="dot"]').val('').prop('disabled', true)
      frm.find('[name="doc"]').prop('disabled', true)
      frm.find('[name="doc"]').closest('.form-group').find('label').removeClass('required')
      frm.find('[name="dolp"]').val('').prop('disabled', true)
      frm.find('[name="soc"]').val('').prop('disabled', true)
      frm.find('[name="doret"]').prop('disabled', true)
      frm.find('[name="doret"]').closest('.form-group').find('label').removeClass('required')
      frm.find('[name="auth"]').val('').prop('disabled', false)
      frm.find('[name="act"]').val('').prop('disabled', false)
      frm.find('[name="vacant"]').val('').prop('disabled', false)
      frm.find('[name="cti"]').val('').prop('disabled', false)
      frm.find('[name="cos"]').val('').prop('disabled', false)
      break;
    default:
      frm.find('[name="afpsn"]').prop('required', true).prop('readonly', false)
      frm.find('[name="afpsn"]').closest('.form-group').find('label').addClass('required')
      frm.find('[name="item_no"]').prop('required', false).prop('readonly', true)
      frm.find('[name="item_no"]').closest('.form-group').find('label').removeClass('required')
      frm.find('[name="bos"] option[value][data-ms=CHR]').prop('disabled', true)
      frm.find('[name="position"]').prop('disabled', true)
      frm.find('[name="fos"]').val('').prop('disabled', false)
      frm.find('[name="daghq"]').val('').prop('disabled', false)
      frm.find('[name="dapda"]').val('').prop('disabled', false)
      frm.find('[name="rrfcd"]').val('').prop('disabled', false)
      frm.find('[name="skills"]').val('').prop('disabled', false)
      frm.find('[name="dot"]').val('').prop('disabled', false)
      frm.find('[name="doc"]').prop('disabled', false)
      frm.find('[name="doc"]').closest('.form-group').find('label').addClass('required')
      frm.find('[name="dolp"]').val('').prop('disabled', false)
      frm.find('[name="soc"]').val('').prop('disabled', false)
      frm.find('[name="doret"]').prop('disabled', false)
      frm.find('[name="doret"]').closest('.form-group').find('label').addClass('required')
      frm.find('[name="auth"]').val('').prop('disabled', true)
      frm.find('[name="act"]').val('').prop('disabled', true)
      frm.find('[name="vacant"]').val('').prop('disabled', true)
      frm.find('[name="cti"]').val('').prop('disabled', true)
      frm.find('[name="cos"]').val('').prop('disabled', true)
      if (val == 'EP') {
        frm.find('[name="rank"] option[value]:not([data-type=EP])').prop('disabled', true)
        frm.find('[name="bos"] option[value][data-ms=TAS]').prop('disabled', true)          
        frm.find('[name="first_name"]').removeClass('text-uppercase')
        frm.find('[name="middle_name"]').removeClass('text-uppercase')
        frm.find('[name="last_name"]').removeClass('text-uppercase')
        frm.find('[name="ext_name"]').removeClass('text-uppercase')
      } else {
        frm.find('[name="rank"] option[value]:not([data-type=Officer])').prop('disabled', true)          
        frm.find('[name="first_name"]').addClass('text-uppercase')
        frm.find('[name="middle_name"]').addClass('text-uppercase')
        frm.find('[name="last_name"]').addClass('text-uppercase')
        frm.find('[name="ext_name"]').addClass('text-uppercase')
      }
      break;
  }
}

$(document).ready(function () {

  $('#tbl_data').on('initComplete', function (event, table) {
    $(this).closest('.card').find('.card-header #organic-tab').text('Organic Personnel'+(table.fnSettings().fnRecordsTotal() > 0 ? ' (' + table.fnSettings().fnRecordsTotal() + ')' : ''))
    $(this).closest('.dataTables_wrapper').find('.dataTables_filter').empty()
    $(this).closest('.dataTables_wrapper').find('.dataTables_length').append('<button id="create-data" class="btn btn-primary float-right" type="button" name="button"><i class="fas fa-plus"></i> Add New</button>')

    $("#create-data").modalForm({
      formURL: "create/"
    });
  });
  
  $('#tbl_data').on('draw.dt', function (table, settings) {
    $(this).find(".update-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });

    $(this).find(".delete-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, modalID: "#modal-sm" });
    });

    $(this).find(".view-orders").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), modalID: "#modal-sm" });
    });
  });

  AjaxDatatableViewUtils.initialize_table(
    $('#tbl_data'),
    "organic/",
    {
      processing: false,
      autoWidth: false,
      full_row_select: false,
      scrollX: false
    }, {},
  );

  $('#frm-upload').on('submit', function(e){
    e.preventDefault()
    var form = this;
    Confirm.fire({
      title: 'Are you sure?',
      text: "You are about to upload a file. This action is irreversible. Do you want to proceed?",
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Yes, upload it!',
      cancelButtonText: 'No, cancel!',
      reverseButtons: true
    }).then((result) => {
      if (result.value) {
        form.submit()
      }
    })
  })

  // Subunits
  $('#tbl_subunits').on('initComplete', function (event, table) {
    $(this).closest('.card').find('.card-header #subunits-tab').text('Personnel from Sub-units'+(table.fnSettings().fnRecordsTotal() > 0 ? ' (' + table.fnSettings().fnRecordsTotal() + ')' : ''))
    $(this).closest('.dataTables_wrapper').find('.dataTables_filter').empty()
  });
  
  $('#tbl_subunits').on('draw.dt', function (table, settings) {
    $(this).find(".view-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });

    $(this).find(".delete-subunit").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, modalID: "#modal-sm" });
    });
  });

  AjaxDatatableViewUtils.initialize_table(
    $('#tbl_subunits'),
    "subunit/",
    {
      processing: false,
      autoWidth: false,
      full_row_select: false,
      scrollX: false
    }, {},
  );

  // DS
  $('#tbl_ds').on('initComplete', function (event, table) {
    $(this).closest('.card').find('.card-header #ds-tab').text('DS From Other Units'+(table.fnSettings().fnRecordsTotal() > 0 ? ' (' + table.fnSettings().fnRecordsTotal() + ')' : ''))
    $(this).closest('.dataTables_wrapper').find('.dataTables_filter').empty()
    $(this).closest('.dataTables_wrapper').find('.dataTables_length').append('<button id="create-ds" class="btn btn-primary float-right" type="button" name="button"><i class="fas fa-plus"></i> Add New</button>')
    
    $("#create-ds").modalForm({
      formURL: "create-ds/",
      modalID: "#modal-sm"
    });
  });
  
  $('#tbl_ds').on('draw.dt', function (table, settings) {
    $(this).find(".view-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });

    $(this).find(".delete-ds").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, modalID: "#modal-sm" });
    });
  });

  AjaxDatatableViewUtils.initialize_table(
    $('#tbl_ds'),
    "ds/",
    {
      processing: false,
      autoWidth: false,
      full_row_select: false,
      scrollX: false
    }, {},
  );

  // School
  $('#tbl_students').on('initComplete', function (event, table) {
    $(this).closest('.card').find('.card-header #students-tab').text('Students'+(table.fnSettings().fnRecordsTotal() > 0 ? ' (' + table.fnSettings().fnRecordsTotal() + ')' : ''))
    $(this).closest('.dataTables_wrapper').find('.dataTables_filter').empty()
    $(this).closest('.dataTables_wrapper').find('.dataTables_length').append('<button id="create-student" class="btn btn-primary float-right" type="button" name="button"><i class="fas fa-plus"></i> Add New</button>')
    
    $("#create-student").modalForm({
      formURL: "create-student/",
      modalID: "#modal-sm"
    });
  });

  AjaxDatatableViewUtils.initialize_table(
    $('#tbl_students'),
    "students/",
    {
      processing: false,
      autoWidth: false,
      full_row_select: false,
      scrollX: false
    }, {},
  );
  
  $('#tbl_students').on('draw.dt', function (table, settings) {
    $(this).find(".view-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });

    $(this).find(".delete-student").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, modalID: "#modal-sm" });
    });
  });

  // Medical
  $('#tbl_patients').on('initComplete', function (event, table) {
    $(this).closest('.card').find('.card-header #patients-tab').text('Patients'+(table.fnSettings().fnRecordsTotal() > 0 ? ' (' + table.fnSettings().fnRecordsTotal() + ')' : ''))
    $(this).closest('.dataTables_wrapper').find('.dataTables_filter').empty()
    $(this).closest('.dataTables_wrapper').find('.dataTables_length').append('<button id="create-patient" class="btn btn-primary float-right" type="button" name="button"><i class="fas fa-plus"></i> Add New</button>')
    
    $("#create-patient").modalForm({
      formURL: "create-patient/",
      modalID: "#modal-sm"
    });
  });

  AjaxDatatableViewUtils.initialize_table(
    $('#tbl_patients'),
    "patients/",
    {
      processing: false,
      autoWidth: false,
      full_row_select: false,
      scrollX: false
    }, {},
  );
  
  $('#tbl_patients').on('draw.dt', function (table, settings) {
    $(this).find(".view-data").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url") });
    });

    $(this).find(".delete-patient").each(function () {
      $(this).modalForm({ formURL: $(this).data("form-url"), isDeleteForm: true, modalID: "#modal-sm" });
    });
  });

  $.each($('[name="message[]"]'), function(){
    Toast.fire({
      icon: $(this).data('tags'),
      title: $(this).val(),
    });
  })

  $(document).on('show.bs.modal', '#modal', function(){
    var frm = $('#frm-data')
    changeProfile(frm.find('[name="profile"]').val(), frm)
  })

  $(document).on('change', '[name=profile]', function() {
    var frm = $('#frm-data')
    frm.find('[name="rank"] option').prop('disabled', false)
    frm.find('[name="bos"] option').prop('disabled', false)
    frm.find('[name="rank"]').val('').change()
    frm.find('[name="bos"]').val('').change()
    frm.find('[name="position"]').val('').change()
    frm.find('[name="afpsn"]').val('')
    frm.find('[name="item_no"]').val('')
    frm.find('[name="doc"]').val('')
    frm.find('[name="doret"]').val('')
    changeProfile($(this).val(), frm)
  })
});