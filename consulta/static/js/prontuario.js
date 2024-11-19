document.getElementById('rg').addEventListener('input', function (event) {
    var input = event.target;
    var value = input.value.replace(/\D/g, ''); // Remove tudo que não for número

    // Limita o valor a 9 caracteres
    if (value.length > 9) {
        value = value.substring(0, 9); // Garante que o valor tenha no máximo 9 caracteres
    }

    // Aplica a máscara apenas se a quantidade de números for adequada
    value = value.replace(/^(\d{2})(\d{0,3})(\d{0,3})(\d{0,2})?$/, function (_, c1, c2, c3, c4) {
        if (c4) {
            return c1 + '.' + c2 + '.' + c3 + '-' + c4;
        }
        if (c3) {
            return c1 + '.' + c2 + '.' + c3;
        }
        if (c2) {
            return c1 + '.' + c2;
        }
        return value;
    });

    input.value = value; // Atualiza o valor do campo
});
