document.addEventListener('DOMContentLoaded', function() {
  const emailBtn = document.querySelector('.email-btn');
  const emailInput = document.querySelector('.email-input');
  const submitBtn = document.querySelector('.submit-btn');
  const errorMessage = document.getElementById('error-message');
  const personalDataCheckbox = document.getElementById('personal-data');
  const messageContainer = document.getElementById('message-container');
  const userEmailSpan = document.getElementById('user-email');

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

    const domain = emailValue.split('@')[1].toLowerCase();
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

  emailBtn.addEventListener('click', () => {
    emailBtn.style.display = 'none';
    emailInput.style.display = 'block';
    submitBtn.style.display = 'block';
  });

  emailInput.addEventListener('blur', validateEmail);

  submitBtn.addEventListener('click', function(event) {
    event.preventDefault();

    const emailIsValid = validateEmail();
    const isChecked = personalDataCheckbox.checked;
    const checkboxError = document.getElementById('checkbox-error');

    checkboxError.style.display = 'none';

    if (!isChecked) {
      checkboxError.style.display = 'block';
      return;
    }

    // Если email валидный и согласие получено, отправляется запрос на сервер
    if (emailIsValid) {
      const email = emailInput.value.trim();

      // Отправка запроса на сервер
      fetch('/send_email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          // Отображение сообщения
          userEmailSpan.textContent = email;
          messageContainer.style.display = 'flex';
        } else {
          // Отображение ошибки от сервера
          alert(data.message || 'Произошла ошибка при отправке письма.');
        }
      })
      .catch((error) => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке письма.');
      });
    }
  });

  // Закрытие сообщения при клике вне формы
  messageContainer.addEventListener('click', function(e) {
    if (e.target === messageContainer) {
      messageContainer.style.display = 'none';
    }
  });
});
