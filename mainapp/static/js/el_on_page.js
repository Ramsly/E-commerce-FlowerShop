window.addEventListener("DOMContentLoaded", () => {
	$(".burger").click(function () {
		$(".burger").toggleClass("active");
	});

	$(".popup__open").click(function () {
		$(".popup").addClass("popup_active");
		$("body").css("overflow", "hidden");
	});

	$(".popup__close").click(function () {
		$(".popup").removeClass("popup_active");
		$("body").css("overflow", "visible");
	});

	$(".main__third_heart_button").click(function () {
		$(".main__third_heart_button").toggleClass("added-to-wish");
	});
});