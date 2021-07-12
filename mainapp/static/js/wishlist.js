// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');

// function csrfSafeMethod(method) {
// 	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }

// $.ajaxSetup({
// 	beforeSend: (xhr, settings) => {
// 		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
// 			xhr.setRequestHeader("X-CSRFToken", csrftoken);
// 		}
// 	},
// });

// const add_to_favorites_url = "/wishlist/add/";
// const remove_from_favorites_url = "/wishlist/remove/";
// const wishlist_api_url = "/wishlist/api/";
// const added_to_favorites_class = "added";


// function add_to_wishlist() {
// 	$("#addToWislist").each((index, el) => {
// 		$(el).click((e) => {
// 			e.preventDefault();

// 			const id = $(el).attr("data-id");
//             const price = $(el).attr("data-price")

// 			if ($(e.target).hasClass(added_to_favorites_class)) {
// 				$.ajax({
// 					url: remove_from_favorites_url,
// 					type: "POST",
// 					dataType: "json",
// 					data: {
// 						qty: 1,
// 						id: id,
//                         price: price
// 					},
// 					success: (data) => {
// 						$(el).removeClass(added_to_favorites_class);
// 						get_session_wishlist();
// 					},
// 				});
// 			} else {
// 				$.ajax({
// 					url: add_to_favorites_url,
// 					type: "POST",
// 					dataType: "json",
// 					data: {
// 						qty: 1,
// 						id: id,
//                         price: price
// 					},
// 					success: (data) => {
// 						$(el).addClass(added_to_favorites_class);
// 						get_session_wishlist();
// 					},
// 				});
// 			}
// 		});
// 	});
// }

// function get_session_wishlist() {
// 	$.getJSON(wishlist_api_url, (json) => {
// 		if (json !== null) {
// 			for (let i = 0; i < json.length; i++) {
// 				$("#addToWislist").each((index, el) => {
// 					const id = $(el).data("id");

// 					if (json[i].id == id) {
// 						$(el).addClass(added_to_favorites_class);
// 					}
// 				});
// 			}
// 		}
// 	});
// }

// $(document).ready(function () {
// 	add_to_wishlist();
// 	get_session_wishlist();
// });


