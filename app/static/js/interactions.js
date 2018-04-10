// add something if we need some interaction in javascript.
  // var elem = document.querySelector('select');
  // var instance = M.FormSelect.init(elem, options);

  // Or with jQuery

$(document).ready(function(){
	// $('select').formSelect();

	var shoplist = {};

	shoplist.name = "Your shopping cart";
	shoplist.list = [
		{name: "Candy 1",price: 30},
		{name: "Candy 2",price: 90},
		{name: "Candy 3",price: 55}
	];

	var item_html = "<tr id={{id}} class='buy_item'><td>{{item}}</td><td class='qty'>{{qty}}</td><td class='price'>{{price}}</td><td id={{del_id}} data-del-id='{{delid}}' class='del_btn'>Remove Item</td></tr>";

	var total_html="<tr class='buy_item total'><td>Total Price</td><td></td><td class='price'>{{price}}</td></tr>";

	function showlist(){
		$("#items_list").html("");
		var total_price = 0;

		for(var i=0; i<shoplist.list.length; i++){
			var item = shoplist.list[i];
			var item_id = "buyitem_" + i;
			var del_item_id = "del_buyitem_" + i;

			total_price += parseInt(item.price);

			var current_item_html = item_html.replace("{{num}}", i+1).replace("{{item}}", item.name).replace("{{id}}", item_id).replace("{{del_id}}", del_item_id).replace("{{price}}", item.price).replace("{{delid}}", i);

			$("#items_list").append(current_item_html);
			$("#"+del_item_id).click(
				function(){
					remove_item($(this).attr("data-del-id"));
				});
		}

		var current_total_html = total_html.replace("{{price}}", total_price);
		$("#items_list").append(current_total_html);
	};

	showlist();

	$(".btn").click(
		function(){
			shoplist.list.push(
				{
					name: $("#test_name").val(),
					price: $("#test_price").val()
				}
			);
			showlist();
		});

	function remove_item(id){
		shoplist.list.splice(id,1);
		showlist();
	};

});