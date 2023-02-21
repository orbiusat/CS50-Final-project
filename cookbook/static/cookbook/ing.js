document.addEventListener('click', event => {
    const element = event.target;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (element.className === 'del-ing') {
        element.parentElement.remove()
        fetch(`delete/ing/${element.parentElement.children[1].innerHTML}`, {
            headers: {'X-CSRFToken': csrftoken},
            method: 'POST',
            mode: 'same-origin'
        })
        .then(response => response.json())
        .then(result => {console.log(result)})

    }
})
   
