document.addEventListener("DOMContentLoaded", function () {
    function showSection(sectionId) {
        // Remove a classe 'active' de todas as seções
        document.querySelectorAll('.config-section').forEach(section => {
            section.classList.remove('active');
        });

        // Adiciona a classe 'active' à seção correspondente
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    }

    // Alternar entre seções ao clicar no menu lateral
    document.querySelectorAll('.config-option').forEach(option => {
        option.addEventListener("click", function (e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });

    // Exibe a seção "Editar Perfil" por padrão
    showSection("editarPerfil");
});
