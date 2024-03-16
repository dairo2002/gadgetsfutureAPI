$(document).ready(function () {
    $('#tblProductos').DataTable({

        "buttons": [
            'copy', 'csv', 'excel', 'pdf', 'print' // Agregar botones de exportación
        ]
    });

});

