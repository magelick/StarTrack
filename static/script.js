const emailBtn = document.querySelector('.email-btn');
const emailInput = document.querySelector('.email-input');
const submitBtn = document.querySelector('.submit-btn');
const messageContainer = document.getElementById('message-container');
const userEmail = document.getElementById('user-email');
const formContainer = document.querySelector('.form-container');

emailBtn.addEventListener('click', () => {
  emailBtn.style.display = 'none';
  emailInput.style.display = 'block';
  submitBtn.style.display = 'block';
});

document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('email-input');
  const errorMessage = document.getElementById('error-message');
  const allowedDomains = ['gmail.com', 'yahoo.com', 'example.com', 'mail.ru', 'icloud.com'];

  function validateEmail() {
    const emailValue = emailInput.value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (emailValue === '') {
      emailInput.classList.remove('error');
      errorMessage.style.display = 'none';
      return false;
    }

    if (!emailPattern.test(emailValue)) {
      emailInput.classList.add('error');
      errorMessage.textContent = 'Неверный формат email';
      errorMessage.style.display = 'block';
      return false;
    }

    const domain = emailValue.split('@')[1];

    if (!allowedDomains.includes(domain)) {
      emailInput.classList.add('error');
      errorMessage.textContent = 'Недопустимый домен';
      errorMessage.style.display = 'block';
      return false;
    }

    emailInput.classList.remove('error');
    errorMessage.style.display = 'none';
    return true;
  }

  emailInput.addEventListener('blur', validateEmail);

  submitBtn.addEventListener('click', function(event) {
      event.preventDefault();

      if (validateEmail()) {
          formContainer.style.display = 'none';
          messageContainer.style.display = 'flex';
          userEmail.textContent = emailInput.value;
      }
  });
});

// Появление строчки с ссылкой "Нажми сюда"
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    document.getElementById('resend-link').style.display = 'block';
  }, 5000);

  // Обработчик клика по ссылке "Нажми сюда"
  document.getElementById('resend-action').addEventListener('click', function(event) {
    event.preventDefault();
    var messageContainer = document.getElementById('message-container');
    messageContainer.style.display = 'block';
    messageContainer.style.opacity = '1';
  });
});

document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');
    });
});

// Открытие бокового меню
function toggleMenu() {
    const menu = document.querySelector('.side-menu');
    const dividers = document.querySelectorAll('.divider');

    menu.classList.toggle('open');

    dividers.forEach(divider => {
        divider.classList.toggle('open');
    });
}

