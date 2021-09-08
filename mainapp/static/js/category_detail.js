window.addEventListener("DOMContentLoaded", function () {
	let overlayLeftBtnText = document.querySelectorAll("#overlayLeftBtn");

	if (window.innerWidth >= 768) {
		overlayLeftBtnText.addEventListener("resize", function () {
			this.innerHTML.replace("Заказать", "");
			console.log(":fda");
		});
	}
});
