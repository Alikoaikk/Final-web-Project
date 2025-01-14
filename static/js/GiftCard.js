$(document).ready( function() {

  document.getElementById('dialog').style.display = 'none';
  document.getElementById('Dialog').addEventListener('click', function() {
  
    document.getElementById('dialog').style.display = 'block';
    document.getElementById('mainContent').classList.add('blur'); 
  });

  document.querySelector('.close').addEventListener('click', function() {

    document.getElementById('dialog').style.display = 'none';
    document.getElementById('mainContent').classList.remove('blur'); 
  });


  setTimeout(function() {
    document.querySelector('.animation-container').style.display = 'none';
    document.querySelector('.initial-page').style.display = 'block';
  }, 5000);

$('#20Button').click(function(){
  let discount_value={
    'discount':'20%',
    "code":generateSerial()
  }
  $.ajax({
    url:'/api/giftcard',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(discount_value),
    success:function(){
    }
  })

});
$('#30Button').click(function(){
  let discount_value={
    'discount':'30%',
    "code":generateSerial()
  }
  $.ajax({
    url:'/api/giftcard',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(discount_value),
    success:function(){
    }
  })

});
$('#50Button').click(function(){
  let discount_value={
    'discount':'50%',
    "code":generateSerial()
  }
  $.ajax({
    url:'/api/giftcard',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(discount_value),
    success:function(){
    }
  })

});
});


function generateSerial() {
  function generateBlock(length) {
    let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let block = '';
    for (let i = 0; i < length; i++) {
      let randomIndex = Math.floor(Math.random() * chars.length);
      block += chars[randomIndex];
    }
    return block;
  }

  let serial = generateBlock(4) + '-' + generateBlock(3) + '-' + generateBlock(3) + '-' + generateBlock(4);
  return serial;
}



