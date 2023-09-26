$(document).ready(function() {
    // Fetch the residence list data from the server
    $.ajax({
        url: '/residence_list_data',
        method: 'GET',
        success: function(data) {
            // Create table header
            var table = '<table border="1"><thead><tr><th>Name</th><th>Room No</th><th>Email</th></tr></thead><tbody>';

            // Loop through the list and append rows to the table
            for (var i = 0; i < data.length; i++) {
                table += '<tr><td>' + data[i].name + '</td><td>' + data[i].room_no + '</td><td>' + data[i].email + '</td></tr>';
            }

            // Close table tags
            table += '</tbody></table>';

            // Append table to the list_residence div
            $('#list_residence').html(table);
        }
    });
});
