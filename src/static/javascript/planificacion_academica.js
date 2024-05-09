document.addEventListener('DOMContentLoaded', function() {
    var formFields = document.querySelectorAll('input, select, textarea');
    formFields.forEach(function(field) {
        field.addEventListener('keypress', function(event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                var index = Array.prototype.indexOf.call(formFields, field);
                var nextField = formFields[index + 1];
                if (nextField) {
                    nextField.focus();
                }
            }
        });
    });
});