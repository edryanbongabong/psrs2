function resetSrc(src) {
  var src = src.split('?')[0];
  return src;  
}
$(document).ready(function () {

  $(document).on('submit', '#frm_data', function (e) {
    e.preventDefault();
    var date = $("#id_date").val();
    $("#frame-organic").attr('src', resetSrc($("#frame-organic").attr('src'))+'?date='+date);
    $("#frame-ds").attr('src', resetSrc($("#frame-ds").attr('src'))+'?date='+date);
    if($('#frame-students').length){
      $("#frame-students").attr('src', resetSrc($("#frame-students").attr('src'))+'?date='+date);
    }
    if($('#frame-patients').length){
      $("#frame-patients").attr('src', resetSrc($("#frame-patients").attr('src'))+'?date='+date);
    }
  });

  $(document).on('submit', '#frm-reports', function (e) {
    e.preventDefault();
    var date = $("#id_date").val();
    if(date == ''){
      Toast.fire({
        icon: 'warning',
        title: 'Please select a date.'
      });
      return;
    }
    var form = this;
    Confirm.fire({
      title: 'Are you sure?',
      text: 'You are about to save a report. Do you want to proceed?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Yes, save it!',
      cancelButtonText: 'No, cancel!',
      reverseButtons: true
    }).then((result) => {
      if (result.value) {
        form.submit();
      }
    });
  });
});