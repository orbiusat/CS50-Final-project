document.addEventListener('click', event => {
    const element = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (element.className === 'del-ing') {
        element.parentElement.remove()

        const cont = document.querySelector('.ing-container')
        if (cont.children.length === 0) {
            console.log('pusto')
            h2 = document.createElement('h2')
            h2.className = 'gr-heading'
            h2.innerHTML = 'You have no ingredients'
            cont.append(h2)
        }

        fetch(`delete/ing/${element.parentElement.children[1].innerHTML}`, {
            headers: {'X-CSRFToken': csrftoken},
            method: 'POST',
            mode: 'same-origin'
        })
        .then(response => response.json())
        .then(result => {console.log(result)})

    }
})
   
