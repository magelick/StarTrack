document.addEventListener('DOMContentLoaded', function() {
  const faqHeaders = document.querySelectorAll('.faq-item-header');

  faqHeaders.forEach(header => {
    header.addEventListener('click', function() {
      const openItem = document.querySelector('.faq-item-content.open');

      // Закрываем уже открытый вопрос и меняем иконку на плюс
      if (openItem && openItem !== this.nextElementSibling) {
        openItem.classList.remove('open');
        openItem.style.maxHeight = null;
        openItem.previousElementSibling.classList.remove('active');
      }

      // Открываем или закрываем текущий вопрос
      const content = this.nextElementSibling;
      if (content.classList.contains('open')) {
        content.classList.remove('open');
        content.style.maxHeight = null;
        this.classList.remove('active');
      } else {
        content.classList.add('open');
        content.style.maxHeight = content.scrollHeight + 'px';
        this.classList.add('active');
      }
    });
  });
});

toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-bottom-right",
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
};
