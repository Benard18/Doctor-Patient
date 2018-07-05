$(document).ready(function () {

	$(".btn").on("click", function (event) {
            if ($(this).hasClass("disabled")) {
                event.stopPropagation()
            } else {
                $('#myModal').modal("show");
            }
        });

	});
