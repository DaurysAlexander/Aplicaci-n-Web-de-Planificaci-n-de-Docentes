document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: [
            // Aquí se cargarían los eventos desde el servidor
        ],
        eventClick: function(info) {
            alert('Evento: ' + info.event.title);
        },
        select: function(info) {
            var startDate = info.startStr;
            var endDate = info.endStr;
            var eventName = prompt('Nombre del Evento:');
            if (eventName) {
                calendar.addEvent({
                    title: eventName,
                    start: startDate,
                    end: endDate
                });

                // Formatea la fecha para que sea compatible con FullCalendar (YYYY-MM-DD)
                var formattedDate = startDate.split('-').reverse().join('/');

                // Envía el evento al servidor
                fetch('/add_event', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({
                        'title': eventName,
                        'start_date': formattedDate,
                        'end_date': formattedDate
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message); // Muestra el mensaje de éxito en la consola
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        }
    });
    calendar.render();

    var eventForm = document.getElementById('eventForm');
    eventForm.addEventListener('submit', function(event) {
        event.preventDefault();
        var eventName = document.getElementById('eventName').value;
        var eventDate = document.getElementById('eventDate').value;

        // Formatea la fecha para que sea compatible con FullCalendar (YYYY-MM-DD)
        var formattedDate = eventDate.split('/').reverse().join('-');

        calendar.addEvent({
            title: eventName,
            start: formattedDate,
            end: formattedDate
        });

        // Envía el evento al servidor
        fetch('/add_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'title': eventName,
                'start_date': formattedDate,
                'end_date': formattedDate
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Muestra el mensaje de éxito en la consola
        })
        .catch(error => {
            console.error('Error:', error);
        });

        eventForm.reset();
    });
});
