function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function (){
    $("#cartAdd").submit(function (event){
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/cart/add",
            headers: {
            'X-CSRFToken': csrftoken
            },
            data:{
                id: $("#id").val(),
                title: $("#price").val(),
                price: $("#title").val(),
            },
            success: function () {
                alert("Продукт добавлен!")
            },
            error: function (){
                console.log(JSON)
            },
        })
        return false;
    })
})





