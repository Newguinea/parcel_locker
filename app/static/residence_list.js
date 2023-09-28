$(document).ready(function () {
    // Fetch the residence list data from the server
    $.ajax({
        url: '/residence_list_data',
        method: 'GET',
        success: function (data) {
            var table = '<table border="1"><thead><tr><th>Name</th><th>Room No</th><th>Email</th><th>Action</th></tr></thead><tbody>';

            for (var i = 0; i < data.length; i++) {
                table += '<tr id="row-' + data[i].id + '">';
                table += '<td><a href="/residence/' + data[i].id + '" class="edit-link" data-id="' + data[i].id + '">' + data[i].name + '</a></td>';
                table += '<td>' + data[i].room_no + '</td>';
                table += '<td>' + data[i].email + '</td>';
                table += '<td><button class="delete-button" data-id="' + data[i].id + '">Delete</button></td></tr>';
            }


            table += '</tbody></table>';
            $('#list_residence').html(table);

            $('.delete-button').click(function () {
                var id = $(this).data('id');
                $.ajax({
                    url: '/delete_residence/' + id,
                    method: 'POST',
                    success: function (response) {
                        // Remove the row from the table
                        $('#row-' + id).remove();
                        alert('Deleted successfully');
                    },
                    error: function () {
                        alert('An error occurred');
                    }
                });
            });
        }
    });
});
