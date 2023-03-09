const input = document.querySelector(".img-input input")
const inputDiv = document.querySelector(".img-input")
const img = document.querySelector(".img-container img")
const select = document.querySelector('.ing-select')
const multiselect = document.querySelector('.multiselect')
const text = multiselect.innerHTML;

// Update selected ingrediets in multiselect field
document.addEventListener('DOMContentLoaded', () => {
    AppendSelectBtn()
})

// Setting image preview div if use upload image by click
input.addEventListener("change", () => {
    const file = input.files
    img.src = URL.createObjectURL(file[0])

})

// Setting image preview div if use upload image by drop
inputDiv.addEventListener("drop", (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files
    img.src = URL.createObjectURL(file[0])
  
})

//Open select field for ingredients
document.querySelector('.multiselect').onclick = () => {
    if (multiselect.dataset.opened === 'False') {
        select.style.display = 'block'
        multiselect.dataset.opened = 'True'
    } else {
        select.style.display = 'none'
        multiselect.dataset.opened = 'False'
    }
}
// Update selected ingrediets in multiselect field on change
select.onchange = () => AppendSelectBtn()


//Creating buttons for selected ingredients
function AppendSelectBtn() {
    let selectedOptions = select.selectedOptions
    multiselect.innerHTML = "";
    for (let option of selectedOptions) {
        let button = document.createElement('button')
        button.type = 'button'
        button.textContent = option.value
        button.style.backgroundColor = option.dataset.color
        button.onclick = () => {
            option.selected = false
            button.remove()
            if (!select.selectedOptions.length) {multiselect.innerHTML = text}
        }
        multiselect.append(button);
    }
    if (!select.selectedOptions.length) {multiselect.innerHTML = text}
}

