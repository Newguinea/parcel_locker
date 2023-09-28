$(document).ready(function () {
    const urlParts = window.location.pathname.split('/');
    const residence_id = urlParts[urlParts.length - 1];
    console.log("Residence ID: ", residence_id);  // Debug line

    if (residence_id) {
        // get information about the residence
        $.ajax({
            url: `/residence_info_get/${residence_id}`,
            method: 'GET',
            success: function (response) {
                $('#first_name').val(response.first_name);
                $('#last_name').val(response.last_name);
                $('#email').val(response.email);
                $('#phone_no').val(response.phone_no);
                $('#unit_num').val(response.unit_num);
                $('#room_no').val(response.room_no);
                $('#nfc_id').val(response.nfc_id);
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
            }
        });
    });
});
