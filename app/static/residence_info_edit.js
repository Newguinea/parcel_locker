$(document).ready(function () {
    const urlParts = window.location.pathname.split('/');
    const residence_id = urlParts[urlParts.length - 1];
    // console.log("Residence ID: ", residence_id);  // Debug line

    if (residence_id) {
        // get information about the residence
        $.ajax({
            url: `/residences/${residence_id}`,
            method: 'GET',
            success: function (response) {
                if (response.data) {
                    $('#first_name').val(response.data.first_name);
                    $('#last_name').val(response.data.last_name);
                    $('#email').val(response.data.email);
                    $('#phone_no').val(response.data.phone_no);
                    $('#unit_num').val(response.data.unit_num);
                    $('#room_no').val(response.data.room_no);
                    $('#nfc_id').val(response.data.nfc_id);
                }
            },
            error: function (jqXHR) {
                if (jqXHR.responseJSON && jqXHR.responseJSON.error && jqXHR.responseJSON.error.message) {
                    alert('Error: ' + jqXHR.responseJSON.error.message);
                } else {
                    alert('An error occurred while fetching the residence info.');
                }
            }
        });
    }

    // submit the changes
    $('#submit').click(function () {
        const data = {
            first_name: $('#first_name').val(),
            last_name: $('#last_name').val(),
            email: $('#email').val(),
            phone_no: $('#phone_no').val(),
            unit_num: $('#unit_num').val(),
            room_no: $('#room_no').val(),
            nfc_id: $('#nfc_id').val()
        };

        $.ajax({
            url: `/edit_residence/${residence_id}`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (response) {
                alert(response.message);
            },
            error: function (jqXHR) {
                if (jqXHR.responseJSON && jqXHR.responseJSON.error && jqXHR.responseJSON.error.message) {
                    alert('Error: ' + jqXHR.responseJSON.error.message);
                } else {
                    alert('An error occurred while updating the residence.');
                }
            }
        });
    });
});

$(document).ready(function() {
    // when click scan button
    $("button[type='button']").click(function() {
        // fetch NFC ID from server
        $.get("/getNFCID", function(data) {
            if (data.status == "success") {
                // if succees, set the value of NFC ID input field
                $("#nfc_id").val(data.NFCid);
            } else {
                // if not success, alert user
                alert("Failed to retrieve NFC ID. Please try again.");
            }
        }).fail(function() {
            alert("Server error. Please try again later.");
        });
    });
});


// route to residence list page
document.getElementById("goBackButton").addEventListener("click", function () {
    window.location.href = "/residence_list";
});