var arrayMonths = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
var hotelId = $("#hotel").data("hotel-id");
var reservation = [];

$(document).ready(function () {
  var monthsSelect = $("#month");
  for (var i = 0; i < 12; i++) {
    monthsSelect.append(`<option value="${arrayMonths[i]}">${arrayMonths[i]}</option>`);
  }

  var daysSelect = $("#day");
  for (var i = 1; i <= 31; i++) {
    daysSelect.append(`<option value="${i}">${i}</option>`);
  }

  var defaultYear = 2024;
  var yearSelect = $("#year");
  for (var i = 0; i < 50; i++) {
    yearSelect.append(`<option value="${defaultYear + i}">${defaultYear + i}</option>`);
  }

  $.ajax({
    url: '/api/getreserve',
    method: 'GET',
    success: function(data) {
      reservation = data;
      console.log(reservation);
    }
  });

  $(document).on('click', '#reserve', function() {
    handleReserve(reservation);
  });
});

function handleReserve(reservations) {
  var price = $("#reserve").data("hotel-price");
  const day = $("#day").val();
  const month = $("#month").val();
  const year = $("#year").val();

  if (day !== "" && month !== "" && year !== "") {
    const date = `${day}/${month}/${year}`;
    let available = true;

    for (let i = 0; i < reservations.length; i++) {
      if (reservations[i].date === date) {
        available = false;
        break;
      }
    }

    if (available) {
      $.ajax({
        url: '/api/reddemgiftcard',
        method: 'GET',
        success: function(data) {
          if (data && !data.usable) {
            if (data.card === "20%") {
              price -= price * 0.2;
            } else if (data.card === "30%") {
              price -= price * 0.3;
            } else {
              price -= price * 0.5;
            }
          }
          makeReservation(hotelId, price, date);
        }
      });
    } else {
      console.log("Date not available");
    }
  }
}

function makeReservation(hotelId, price, date) {
  var reservation = {
    "hotelId": hotelId,
    "price": price,
    "date": date
  };

  $.ajax({
    url: "/api/reserve",
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify(reservation),
    success: function() {
      location.reload();
      console.log("Reservation made successfully");
    }
  });
}
