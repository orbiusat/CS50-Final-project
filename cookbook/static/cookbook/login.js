document.getElementById('register-btn').onclick = () => {
    document.getElementById('register-form').style.display = 'flex';
    document.getElementById('login-form').style.display = 'none';
}

document.getElementById('login-btn').onclick = () => {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'flex';
}