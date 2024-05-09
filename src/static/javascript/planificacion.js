    function handleEnter(event, currentElement) {
        if (event.keyCode === 13) {
            event.preventDefault();
            const form = currentElement.form;
            const index = Array.prototype.indexOf.call(form, currentElement);
            form.elements[index + 1].focus();
            return false;
        }
        return true;
    }
