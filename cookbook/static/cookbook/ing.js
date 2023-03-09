// Handling deleting ingredients
document.addEventListener('click', event => {

    //if user clicks on delete button on ingredient, deleting it from DOM immediately
    const element = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (element.className === 'del-ing') {
        element.parentElement.remove()

        // if there is no more ingredients, create heading that says so 
        const cont = document.querySelector('.ing-container')
        if (cont.children.length === 0) {
            h2 = document.createElement('h2')
            h2.className = 'gr-heading'
            h2.innerHTML = 'You have no ingredients'
            cont.append(h2)
        }
        // Deleting ingredient from database
        fetch(`delete/ing/${element.parentElement.children[1].innerHTML}`, {
            headers: {'X-CSRFToken': csrftoken},
            method: 'POST',
            mode: 'same-origin'
        })
        .then(response => response.json())
        .then(result => {console.log(result)})

    }
})