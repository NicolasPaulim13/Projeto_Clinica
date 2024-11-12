document.getElementById("id_imagem_perfil").addEventListener("change", function(event) {
    const preview = document.querySelector(".profile-image-preview");
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        preview.src = e.target.result;
    };

    if (file) {
        reader.readAsDataURL(file);
    }
});
