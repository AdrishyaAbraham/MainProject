// form visible
$('#academic_info_btn').on('click', function(){
  $('.academic_info').hide();
  // $('.personal_info').show();
  $('.gaurdian_info').show();
  $('#submit').show();
});

// Presonal Information
$('#personal_info_btn').on('click', function(){
  $('.personal_info').hide();
  $('.guardian_info').show();
  
});

$('#personal_info_prev_btn').on('click', function(){
  $('.personal_info').hide();
  $('.academic_info').show();
});


// Guardian Information
$('#guardian_info_btn').on('click', function(){
  $('.guardian_info').hide();
  $('.previous_academic_info').show();
});

$('#guardian_info_prev_btn').on('click', function(){
  $('.guardian_info').hide();
  $('.personal_info').show();
});



// Previous Academic Information
$('#previous_academic_info_btn').on('click', function(){
  $('.previous_academic_info').hide();
  $('.previous_academic_certificate').show();
  $('#submit').show();
});

$('#previous_academic_info_prev_btn').on('click', function(){
  $('.previous_academic_info').hide();
  $('.guardian_info').show();
});

// Previous Academic Certificate Information
$('#previous_academic_certificate_prev_btn').on('click', function(){
  $('.previous_academic_certificate').hide();
  $('.previous_academic_info').show();
});
