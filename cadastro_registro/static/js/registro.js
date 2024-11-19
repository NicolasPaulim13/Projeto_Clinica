document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registration-form");
  const senhaInput = document.getElementById("senha_paciente");
  const requisitosContainer = document.getElementById("senha-requisitos");

  const requisitoMinLength = document.querySelector(".requisito-min-length");
  const requisitoNumber = document.querySelector(".requisito-number");
  const requisitoSpecialChar = document.querySelector(".requisito-special-char");

  // Validação de requisitos de senha em tempo real
  function verificarRequisitos() {
    const senha = senhaInput.value;

    // Validação de tamanho mínimo
    requisitoMinLength.style.color = senha.length >= 8 ? "green" : "red";

    // Validação de número
    requisitoNumber.style.color = /\d/.test(senha) ? "green" : "red";

    // Validação de caractere especial
    requisitoSpecialChar.style.color = /[!@#$%^&*(),.?":{}|<>]/.test(senha) ? "green" : "red";
  }

  // Mostra os requisitos após tentativa de envio inválida
  form.addEventListener("submit", function (event) {
    const senha = senhaInput.value;
    let valid = true;

    if (senha.length < 8 || !/\d/.test(senha) || !/[!@#$%^&*(),.?":{}|<>]/.test(senha)) {
      valid = false;
    }

    if (!valid) {
      requisitosContainer.classList.remove("hidden");
      event.preventDefault();
    }
  });

  senhaInput.addEventListener("input", verificarRequisitos);

  // Máscara e validação de CPF
  const cpfInput = document.getElementById("cpf_paciente");

  cpfInput.addEventListener("input", function (event) {
    let value = event.target.value.replace(/\D/g, ""); // Remove caracteres não numéricos
    if (value.length > 3) value = value.replace(/^(\d{3})(\d)/, "$1.$2");
    if (value.length > 6) value = value.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
    if (value.length > 9) value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
    event.target.value = value.substring(0, 14); // Limita a 14 caracteres no input
  });

  // Remover máscara ao sair do campo (opcional, pois o valor é ajustado automaticamente no envio)
  cpfInput.addEventListener("blur", function () {
    const value = cpfInput.value.replace(/\D/g, ""); // Retira qualquer formatação
    if (value.length !== 11) {
      alert("CPF inválido. Por favor, revise.");
    }
  });

});
