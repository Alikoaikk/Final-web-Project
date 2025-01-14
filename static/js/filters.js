let countRooms = parseInt($(".countRooms").text());
let countPersons = parseInt($(".countPerson").text());
var hotelData = [];

// ----------------Buttons for rooms-----------------------------
$(document).on('click', '#buttonMinusRoom', function (event) {
  event.preventDefault();
  if (countRooms > 0) {
    countRooms = countRooms - 1;
    $(".countRooms").text(countRooms);
  }
});

$(document).on('click', '#buttonPlusRoom', function (event) {
  event.preventDefault();
  if (countRooms < 20) {
    countRooms = countRooms + 1;
    $(".countRooms").text(countRooms);
  }
});

//--------------------Buttons of the Persons---------------------
$(document).on('click', '#buttonMinusPerson', function (event) {
  event.preventDefault();
  if (countPersons > 0) {
    countPersons = countPersons - 1;
    $(".countPerson").text(countPersons);
  }
});

$(document).on('click', '#buttonPlusPerson', function (event) {
  event.preventDefault();
  if (countPersons < 20) {
    countPersons = countPersons + 1;
    $(".countPerson").text(countPersons);
  }
});

//----------------Filter function-----------------
let privlgs = $("input[type=checkbox]");
let privArray = [];
let filteredArray = [];

$(document).on('click', '#filterButton', function () {
  privArray = [];
  let numRoom=parseInt($(".countRooms").text());
  let numPeople=parseInt($(".countPerson").text());
  console.log(numRoom)
  console.log(numPeople)
  for (let i = 0; i < privlgs.length; i++) {
    if (privlgs[i].checked) {
      let checkboxId = privlgs[i].id;
      privArray.push(checkboxId);
    }
  }

  $.ajax({
    url: "/api/all_hotels",
    method: 'GET',
    success: function (data) {
      hotelData = data;
      console.log(hotelData);
      filteredArray = hotelData.filter(hotel => {
        const privilegesPassed = privArray.every(priv => {
          console.log(`Hotel privilege ${priv}:`, hotel[priv]);
          return hotel[priv] == 1;
        });
        console.log(hotel.maxNumPeop);
        const roomsPassed = hotel.maxNumRoom>= numRoom;
        console.log("Hotel maxNumRoom:", hotel.maxNumRoom);
        const peoplePassed = hotel.maxNumPeop >= numPeople;
        console.log("Hotel maxNumPeop:", hotel.maxNumPeop);

        return privilegesPassed && roomsPassed && peoplePassed;
      });

      console.log("Filtered hotels:", filteredArray);
      getCards(filteredArray);
    }
  });
});

$(document).on('click', '.card', function () {
  const hotelId = $(this).data("hotel-id");
  $.ajax({
    url: `/api/gethotel/${hotelId}`,
    method: 'GET',
    success: function (data) {
      window.location.href = `/detail/${hotelId}`;
    }
  });
});

function getCards(list) {
  $(".filteredCards").empty();
  for (let i = 0; i < list.length; i++) {
    $(".filteredCards").append(addCard(list[i]));
  }
}

function addCard(data) {
  return `
    <div class="card" data-hotel="${data.placeName}" data-hotel-id="${data.placeId}">
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
}
