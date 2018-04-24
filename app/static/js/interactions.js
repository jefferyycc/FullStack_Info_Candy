// add something if we need some interaction in javascript.
// var elem = document.querySelector('select');
// var instance = M.FormSelect.init(elem, options);

// Or with jQuery

$(document).ready(function(){

	$('.carousel.carousel-slider').carousel({
		fullWidth: true,
		indicators: true
	});

	setInterval(function(){
		$('.carousel.carousel-slider').carousel('next');
		},2000);

	var elem = document.querySelector('.fixed-action-btn');

	var instance = M.FloatingActionButton.init(elem, {
		direction: 'left',
		hoverEnabled: false
	});

	$('.parallax').parallax();

	$('select').formSelect();

});

function addItem() {
	url = "http://0.0.0.0:8081/get_email";
    var req = new XMLHttpRequest();
    req.open('POST', url, true);

    req.onload = function() {
		if (req.status === 200) {
			var data = JSON.parse(req.responseText);
			var email = data["email"];
			if (!(localStorage.getItem('shoppingCart'))){
				// initialize shoppingCart in localStorage
				localStorage.setItem('shoppingCart', JSON.stringify({}));
			}
			var shoppingCart = JSON.parse(localStorage.shoppingCart);
			// if the email is not in the localStorage.shoppingCart
			// initialize for the email.
			if (!(email in shoppingCart)) {
				shoppingCart[email] = {"boxes" : {}, "totalPrice" : 0};
				localStorage.shoppingCart=JSON.stringify(shoppingCart);	
			}
		} else {
			alert(req.status);
		}

		var item_html = "<tr id={{id}} class='buy_item'><td>{{item}}</td><td class='qty'>{{qty}}</td><td class='price'>{{price}}</td><td id={{del_id}} data-del-id='{{delid}}' class='del_btn'>Remove Item</td></tr>";

		var total_html="<tr class='buy_item total'><td>Total Price</td><td></td><td class='price'>{{price}}</td></tr>";

		// show shopping cart
		function showlist(){

			$("#displayshoppingcart").html("");

			var itemName = Object.keys(shoppingCart[email]['boxes']);
			var itemQty = Object.values(shoppingCart[email]['boxes']);
			var itemPrice = Object.values(shoppingCart[email]['boxprice']);
			for (i=0; i<itemName.length; i++) {
				var item = itemName[i];
				var qty = itemQty[i];
				var price = itemPrice[i];
				var item_id = "buyitem_" + i;
				var del_item_id = "del_buyitem_" + i;

				total_price = shoppingCart[email]['totalPrice'];

				var current_item_html = item_html.replace("{{item}}", item).replace("{{id}}", item_id).replace("{{qty}}", qty).replace("{{del_id}}", del_item_id).replace("{{price}}", price).replace("{{delid}}", i);

				$("#displayshoppingcart").append(current_item_html);

				$("#"+del_item_id).click(
					function(){
						id = $(this).attr("data-del-id")
						delete shoppingCart[email]['boxes'][itemName[id]]
						delete shoppingCart[email]['boxprice'][id]
						localStorage.shoppingCart=JSON.stringify(shoppingCart);
						showlist();
					});
			}

			var current_total_html = total_html.replace("{{price}}", total_price);
			$("#displayshoppingcart").append(current_total_html);
		}

		showlist();
    };

    req.send();
}

// add default boxes into shopping cart.
function addCartDefault() {
	url = "http://0.0.0.0:8081/get_email";
    var req = new XMLHttpRequest();
    req.open('POST', url, true);

    req.onload = function() {
		if (req.status === 200) {
			var data=JSON.parse(req.responseText);
			var email = data["email"];
			var shoppingCart = JSON.parse(localStorage.shoppingCart);
			// input: six qty pref1, prf2 ..., for following default boxes:
			// ["10000000", "00100000", "00001000", "00000010", "05050500", "05000505"]
			var pref1 = parseInt($("#pref1 option:selected").val());
			var pref2 = parseInt($("#pref2 option:selected").val());
			var pref3 = parseInt($("#pref3 option:selected").val());
			var pref4 = parseInt($("#pref4 option:selected").val());
			var pref5 = parseInt($("#pref5 option:selected").val());
			var pref6 = parseInt($("#pref6 option:selected").val());

			var box = shoppingCart[email]["boxes"];
			if (pref1 !== 0 && !!pref1) {
				box["10000000"] = "10000000" in box ? box["10000000"] + pref1 : pref1;
			}
			if (pref2 !== 0 && !!pref2) {
				box["00100000"] = "00100000" in box ? box["00100000"] + pref2 : pref2;
			}
			if (pref3 !== 0 && !!pref3) {
				box["00001000"] = "00001000" in box ? box["00001000"] + pref3 : pref3;
			}
			if (pref4 !== 0 && !!pref4) {
				box["00050505"] = "00050505" in box ? box["00050505"] + pref4 : pref4;
			}
			if (pref5 !== 0 && !!pref5) {
				box["05050500"] = "05050500" in box ? box["05050500"] + pref5 : pref5;
			}
			if (pref6 !== 0 && !!pref6) {
				box["05000505"] = "05000505" in box ? box["05000505"] + pref6 : pref6;
			}

			url_web = "http://0.0.0.0:8081/price_calculate";
		    var req_inside = new XMLHttpRequest();
		    req_inside.open('POST', url_web, false);
		    req_inside.setRequestHeader("Content-type", "application/json");
		    req_inside.onload = function() {
				if (req_inside.status === 200) {
					var data=JSON.parse(req_inside.responseText);
					shoppingCart[email]["boxes"] = box;
					shoppingCart[email]["totalPrice"] = data["price"];
					shoppingCart[email]["boxprice"] = data["itemprice"];
					localStorage.shoppingCart=JSON.stringify(shoppingCart);
				} else {
					alert(req_inside.status);
				}
		    };
		    // await sleep(1000);
		    req_inside.send(JSON.stringify(box));
		} else {
			alert(req.status);
		}
    };
    req.send();
}

// add DIY boxes into shopping cart.
function addCartDIY() {
	url = "http://0.0.0.0:8081/get_email";
    var req = new XMLHttpRequest();
    req.open('POST', url, true);

    req.onload = function() {
		if (req.status === 200) {
			var data=JSON.parse(req.responseText);
			var email = data["email"];
			var shoppingCart = JSON.parse(localStorage.shoppingCart);
			var box = shoppingCart[email]["boxes"];
			var size = parseInt($('input[name="size"]:checked').val());
			var C1 = parseInt($('input[name="flavor1"]').val());
			var C2 = parseInt($('input[name="flavor2"]').val());
			var C3 = parseInt($('input[name="flavor3"]').val());
			var C4 = parseInt($('input[name="flavor4"]').val());

			Number.prototype.pad = function(size) {
			  var s = String(this);
			  while (s.length < (size || 2)) {s = "0" + s;}
			  return s;
			};
			var box_id = C1.pad(2).concat(C2.pad(2), C3.pad(2), C4.pad(2));
			var qty = parseInt($("#box-num option:selected").val());
			box[box_id] = box_id in box ? box[box_id] + qty : qty;

			url_web = "http://0.0.0.0:8081/price_calculate";
		    var req_inside = new XMLHttpRequest();
		    req_inside.open('POST', url_web, false);
		    req_inside.setRequestHeader("Content-type", "application/json");

		    req_inside.onload = function() {
				if (req_inside.status === 200) {
					var data=JSON.parse(req_inside.responseText);
					shoppingCart[email]["boxes"] = box;
					shoppingCart[email]["totalPrice"] = data["price"];
					shoppingCart[email]["boxprice"] = data["itemprice"];
					localStorage.shoppingCart=JSON.stringify(shoppingCart);
				} else {
					alert(req_inside.status);
				}
		    };
		    req_inside.send(JSON.stringify(box));
		} else {
			alert(req.status);
		}
    };
    req.send();
}

// place order
function placeOrder() {
	url = "http://0.0.0.0:8081/get_email";
    var req = new XMLHttpRequest();
    req.open('POST', url, true);

    req.onload = function() {
		if (req.status === 200) {
			var data=JSON.parse(req.responseText);
			var email = data["email"];
			var shoppingCart = JSON.parse(localStorage.shoppingCart);
			shoppingCartCurrentUser = shoppingCart[email];
			url_web = "http://0.0.0.0:8081/place_order";
		    var req_inside = new XMLHttpRequest();
		    req_inside.open('POST', url_web, false);
		    req_inside.setRequestHeader("Content-type", "application/json");

		    req_inside.onload = function() {
				if (req_inside.status === 200) {

				} else {
					alert(req_inside.status);
				}
		    };
		    req_inside.send(JSON.stringify(shoppingCartCurrentUser));
		    delete shoppingCart[email];
		    localStorage.shoppingCart=JSON.stringify(shoppingCart);
		} else {
			alert(req.status);
		}
    };
    req.send();
}