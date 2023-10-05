$(document).ready(function() {
    $("#residenceForm").on("submit", function(event) {
        event.preventDefault();

        var formData = {
            "first_name": $("#first_name").val(),
            "last_name": $("#last_name").val(),
            "email": $("#email").val(),
            "phone_no": $("#phone_no").val(),
            "unit_num": parseInt($("#unit_num").val()),
            "room_no": $("#room_no").val(),
            "nfc_id": $("#nfc_id").val()
        };

        $.ajax({
            url: "/residences",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function(response) {
                alert("Residence created successfully");
                $("#residenceForm")[0].reset();
            },
            error: function(jqXHR) {
                if (jqXHR.responseJSON && jqXHR.responseJSON.error && jqXHR.responseJSON.error.message) {
                    alert('Error: ' + jqXHR.responseJSON.error.message);
                } else {
                    alert('An error occurred while trying to create the residence.');
                }
            }
        });
    });
});


// route to residence list page
document.getElementById("goBackButton").addEventListener("click", function() {
  window.location.href = "/residence_list";
});