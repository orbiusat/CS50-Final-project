// Setting height of textarea with recipe instruction depending on among of strings in it 
document.addEventListener("DOMContentLoaded", () => {
    t = document.querySelector('.gr-textarea-text')
    t.style.height = "";
    t.style.height = t.scrollHeight + "px"

    // Handling delete recipe button 
    document.getElementById('delete-btn').onclick = () => {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const name = document.querySelector('#name').dataset.name
        const id = document.querySelector('#name').dataset.id
        const conf = confirm(`Are you sure you want to delete ${name}?`)
        if (conf) {
            fetch(`/delete/recipe/${id}`, {
                headers: {'X-CSRFToken': csrftoken},
                redirect: 'follow',
                method: 'POST',
                mode: 'same-origin'
            })
            .then(response => window.open(response.url, "_self"))
        }
    }
})


