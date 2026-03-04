// $(document).ready(function () {
//   $('#tbl_data').dataTable({
//     "processing": true,
//     "ajax": {
//       "processing": true,
//       "url": "{% url 'view-ranks' %}",
//       "dataSrc": ""
//     },

//     "columns": [
//       { "data": "rank" },
//       { "data": "rank_full" }
//     ]
//   });
// });

$(document).ready(function() {
  AjaxDatatableViewUtils.initialize_table(
      $('#tbl_data'),
      "all/",
      {
          processing: false,
          autoWidth: false,
          full_row_select: false,
          scrollX: false
      }, {
      },
  );
});