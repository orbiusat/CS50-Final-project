// Switching between Register and Login view
document.getElementById('register-btn').onclick = () => {
    document.getElementById('register-form').style.display = 'flex';
    document.getElementById('login-form').style.display = 'none';
    document.querySelectorAll('.error-p').forEach(Element => {
        Element.remove();
    });
}

document.getElementById('login-btn').onclick = () => {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'flex';
    document.querySelectorAll('.error-p').forEach(Element => {
       Element.remove();
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const state = document.getElementById('register-form').dataset.state
    if (state) {
        document.getElementById('register-form').style.display = 'flex';
        document.getElementById('login-form').style.display = 'none';
    }
})