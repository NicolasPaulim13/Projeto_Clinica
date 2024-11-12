document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    
    form.addEventListener("submit", function (event) {
        if (!confirm("Tem certeza de que deseja salvar as alterações?")) {
            event.preventDefault(); // Cancela o envio do formulário se o usuário não confirmar
        }
    });

    // Exemplo de validação básica
    const dateField = document.querySelector("#id_data_consulta");
    dateField.addEventListener("input", function () {
        const date = new Date(this.value);
        const today = new Date();
        
        if (date < today) {
            this.setCustomValidity("A data da consulta não pode ser no passado.");
            this.reportValidity();
        } else {
            this.setCustomValidity("");
        }
    });
});
