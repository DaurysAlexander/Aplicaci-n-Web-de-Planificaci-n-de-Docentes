document.addEventListener('DOMContentLoaded', function() {
    const agregarMaterialBtn = document.getElementById('agregar-material');
    const tablaMateriales = document.getElementById('tabla-materiales');

    agregarMaterialBtn.addEventListener('click', function() {
        const ultimaFila = tablaMateriales.rows[tablaMateriales.rows.length - 1].cloneNode(true);
        tablaMateriales.appendChild(ultimaFila);
        ultimaFila.querySelector('.eliminar-material').addEventListener('click', function() {
            ultimaFila.remove();
        });
    });

    document.querySelectorAll('.eliminar-material').forEach(btn => {
        btn.addEventListener('click', function() {
            btn.closest('tr').remove();
        });
    });
});