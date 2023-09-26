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
            "nfc_id": $("#nfc_id").val() // can be empty
        };

        $.ajax({
            url: "/residences",  // Flask API endpoint
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function(response) {
                alert("Residence created successfully");
                // clear the form
                $("#residenceForm")[0].reset();
            },
            error: function(error) {
                alert("An error occurred: " + JSON.stringify(error));
            }
        });
    });
});
