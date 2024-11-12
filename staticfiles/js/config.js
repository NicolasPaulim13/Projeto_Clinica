document.addEventListener("DOMContentLoaded", function () {
    function showSection(sectionId) {
        document.querySelectorAll('.config-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
    }

    document.querySelector(".config-option[data-section='editarPerfil']").addEventListener("click", function (e) {
        e.preventDefault();
        showSection("editarPerfil");
    });
    
    document.querySelector(".config-option[data-section='informacoesPessoais']").addEventListener("click", function (e) {
        e.preventDefault();
        showSection("informacoesPessoais");
    });

    // Exibir "Editar Perfil" por padrão ao carregar a página
    showSection("editarPerfil");
});
