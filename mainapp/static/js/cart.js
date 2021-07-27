function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
const csrftoken = getCookie("csrftoken");

$(document).ready(function () {
	$("#cartAdd").submit(function (event) {
		event.preventDefault();
		// if ($("#overlayLeftBtn").hasClass("delete wishlist-del")) {
			$.ajax({
				type: "POST",
				url: "cart/add/",
				dataType: "json",
				headers: {
					"X-CSRFToken": getCookie("csrftoken"),
				},
				data: {
					"id": $("#id").val(),
					"title": $("#title").val(),
					"qty": 1,
					"price": $("#price").val(),
				},
				success: function (json_data) {
					// $("#overlayLeftBtn").removeClass("delete wishlist-del")
					console.log(json_data)
				},
				error: function (json_data) {
					console.log(json_data)
				},
			});
		// } else{
		// 	$.ajax({
		// 		type: "POST",
		// 		url: "/cart/remove/",
		// 		dataType: "json",
		// 		headers: {
		// 			"X-CSRFToken": getCookie("csrftoken"),
		// 		},
		// 		data: {
		// 			"id": $("#id").val(),
		// 			"title": $("#title").val(),
		// 			"qty": 1,
		// 			"price": $("#price").val(),
		// 		},
		// 		success: function () {
		//
		// 		},
		// 		error: function (response) {
		// 			alert("Ошибка!")
		// 		},
		// 	});
		// }
	});
});
