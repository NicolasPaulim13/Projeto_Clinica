
// Pré-visualização da imagem de perfil antes de enviar o formulário
document.getElementById('id_imagem_perfil').addEventListener('change', function(event) {
    const [file] = event.target.files;
    if (file) {
        document.getElementById('previewImagem').src = URL.createObjectURL(file);
    }
});

// Carregar o valor inicial do campo de acessibilidade
document.addEventListener("DOMContentLoaded", function() {
    const acessibilidade = "{{ form.initial.acessibilidade }}";
    const select = document.getElementById("acessibilidadeSelect");
    if (select) {
        select.value = acessibilidade;
    }
});
