// JavaScript para alternar a exibição das respostas nas perguntas frequentes
function toggleResposta(element) {
    const resposta = element.nextElementSibling;
    const icon = element.querySelector('.icon');
    resposta.classList.toggle('active');
    icon.classList.toggle('rotate');
}

// JavaScript para alternar a exibição do menu em dispositivos móveis
const hamburgerMenu = document.querySelector('.hamburger-menu');
const nav = document.querySelector('.nav');

hamburgerMenu.addEventListener('click', () => {
    nav.classList.toggle('active');
});

document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggle = document.getElementById('perfilDropdown');
    const dropdownMenu = document.getElementById('dropdownMenu');
    let isDropdownOpen = false;
  
    // Toggle dropdown when clicking on name or image
    dropdownToggle.addEventListener('click', function (event) {
      event.preventDefault();
      isDropdownOpen = !isDropdownOpen;
      dropdownMenu.classList.toggle('show', isDropdownOpen);
    });
  
    // Toggle individual form within the dropdown
    window.toggleForm = function (event, formId) {
      event.preventDefault();
      const form = document.getElementById(formId);
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
    };
  
    // Close dropdown when clicking outside
    document.addEventListener('click', function (event) {
      if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.remove('show');
        isDropdownOpen = false;
      }
    });
  });
  const accordionButtons = document.querySelectorAll(".accordion-button");

accordionButtons.forEach(button => {
    button.addEventListener("click", () => {
        const content = button.nextElementSibling;

        // Fecha todos os outros conteúdos ao abrir um novo
        document.querySelectorAll(".accordion-content").forEach(item => {
            if (item !== content) {
                item.style.maxHeight = null;
            }
        });

        // Expande ou recolhe o conteúdo
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
});

  