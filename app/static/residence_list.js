$(document).ready(function () {
    // Fetch the residence list data from the server
    $.ajax({
        url: '/residence_list_data',
        method: 'GET',
        success: function (response) {
            if (response.data && Array.isArray(response.data)) {
                var table = '<table border="1"><thead><tr><th>Name</th><th>Room No</th><th>Email</th><th>Action</th></tr></thead><tbody>';

                for (var i = 0; i < response.data.length; i++) {
                    table += '<tr id="row-' + response.data[i].id + '">';
                    table += '<td><a href="/residence/' + response.data[i].id + '" class="edit-link" data-id="' + response.data[i].id + '">' + response.data[i].name + '</a></td>';
                    table += '<td>' + response.data[i].room_no + '</td>';
                    table += '<td>' + response.data[i].email + '</td>';
                    table += '<td><button class="delete-button" data-id="' + response.data[i].id + '">Delete</button></td></tr>';
                }

                table += '</tbody></table>';
                $('#list_residence').html(table);

                $('.delete-button').click(function () {
                    var id = $(this).data('id');
                    $.ajax({
                        url: '/delete_residence/' + id,
                        method: 'POST',
                        success: function () {
                            // Remove the row from the table
                            $('#row-' + id).remove();
                            alert('Deleted successfully');
                        },
                        error: function (jqXHR) {
                            if (jqXHR.responseJSON && jqXHR.responseJSON.error && jqXHR.responseJSON.error.message) {
                                alert('Error: ' + jqXHR.responseJSON.error.message);
                            } else {
                                alert('An error occurred while trying to delete the residence.');
                            }
                        }
                    });
                });

            } else {
                alert('Unexpected data format received.');
            }
        },
        error: function (jqXHR) {
            if (jqXHR.responseJSON && jqXHR.responseJSON.error && jqXHR.responseJSON.error.message) {
                alert('Error: ' + jqXHR.responseJSON.error.message);
            } else {
                alert('An error occurred while fetching the residence list.');
            }
        }
    });
});


// route of logout
document.getElementById("logoutButton").addEventListener("click", function () {
    window.location.href = "/logout";
});
// route to residence info add page
document.getElementById("RegisterResidenceButton").addEventListener("click", function () {
    window.location.href = "/residence_info_add";
});