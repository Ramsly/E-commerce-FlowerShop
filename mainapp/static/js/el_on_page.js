window.addEventListener("DOMContentLoaded", () => {
	let messageCloseBtn = document.querySelector(".message_close");
	messageCloseBtn.addEventListener("click", function () {
        let message = document.querySelector(".message")
		message.style.display = "none";
	});
});
