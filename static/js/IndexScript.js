$(document).ready(function () {
  getCards();
  $(document).on('click', '.card', function () {
    const hotelId=$(this).data("hotel-id");
    $.ajax({
      url:`/api/gethotel/${hotelId}`,
      method:'GET',
      success: function(){
      }
    })
    window.location.href = `/detail/${hotelId}`;
  });
});

function getCards() {
  $.ajax({
    url:'/api/all_hotels',
    method:'GET',
    success:function(data){
      hotelData=data
      for (let i = 0; i < hotelData.length; i++) {
        $(".container").append(addCard(hotelData[i]));
      }
    }
  });
 
}

function addCard(data) {
  newCard = `<div class="card" data-hotel="${data.placeName}"  data-hotel-id="${data.placeId}">
  <div class="backDiv">
    
      <p>${data.placeDescription}<br>
      Price: ${data.placePrice}</p>
    
  </div>
    <div class="img">
      <img src="${data.imgofplace}" alt="">
    </div>

    <div class="tital1">
      <p>${data.placeName}</p>
    </div>

</div>`;
  return newCard;
}
