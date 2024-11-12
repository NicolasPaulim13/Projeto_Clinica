function generateTimeOptions() {
    const selectElement = document.getElementById('hora_consulta');
    const dataConsulta = document.getElementById('data_consulta').value;
    const hoje = new Date();
    const dataSelecionada = new Date(dataConsulta);

    if (selectElement && selectElement.tagName === 'SELECT') {
        selectElement.innerHTML = ''; // Limpa opções existentes

        // Define o horário de início e término
        const start = new Date();
        start.setHours(8, 0, 0, 0); // Início às 08:00
        const end = new Date();
        end.setHours(20, 0, 0, 0); // Fim às 20:00

        // Se a data da consulta for hoje, ajusta o horário inicial para o próximo horário disponível
        if (dataSelecionada.toDateString() === hoje.toDateString()) {
            start.setHours(hoje.getHours(), hoje.getMinutes(), 0, 0);

            // Ajusta o horário para o próximo intervalo de 30 minutos
            if (start.getMinutes() > 0 && start.getMinutes() < 30) {
                start.setMinutes(30);
            } else if (start.getMinutes() > 30) {
                start.setHours(start.getHours() + 1, 0);
            }
        }

        // Cria opções em intervalos de 30 minutos
        for (let time = new Date(start); time <= end; time.setMinutes(time.getMinutes() + 30)) {
            const hours = time.getHours().toString().padStart(2, '0');
            const minutes = time.getMinutes().toString().padStart(2, '0');
            const option = document.createElement('option');
            option.value = `${hours}:${minutes}`;
            option.textContent = `${hours}:${minutes}`;
            selectElement.appendChild(option);
        }
    } else {
        console.warn("Elemento 'hora_consulta' não encontrado ou não é um <select>.");
    }
}

function atualizarDataFormatada() {
    const inputData = document.getElementById('data_consulta').value;
    const data = new Date(inputData);
    
    if (!isNaN(data)) {
        const dia = String(data.getDate()).padStart(2, '0');
        const mes = String(data.getMonth() + 1).padStart(2, '0'); // Janeiro é 0
        const ano = data.getFullYear();
    
        // Formata a data no formato dia/mês/ano
        const dataFormatada = `${dia}/${mes}/${ano}`;
    
        // Exibe a data formatada
        document.getElementById('data_formatada').textContent = `Data selecionada: ${dataFormatada}`;
    }
}

function definirIntervaloData() {
    const hoje = new Date();
    const umAnoDepois = new Date();
    umAnoDepois.setFullYear(hoje.getFullYear() + 1);

    // Define a data mínima (hoje)
    const anoMin = hoje.getFullYear();
    const mesMin = String(hoje.getMonth() + 1).padStart(2, '0');
    const diaMin = String(hoje.getDate()).padStart(2, '0');
    const dataMinima = `${anoMin}-${mesMin}-${diaMin}`;

    // Define a data máxima (um ano a partir de hoje)
    const anoMax = umAnoDepois.getFullYear();
    const mesMax = String(umAnoDepois.getMonth() + 1).padStart(2, '0');
    const diaMax = String(umAnoDepois.getDate()).padStart(2, '0');
    const dataMaxima = `${anoMax}-${mesMax}-${diaMax}`;

    // Atualiza os atributos min e max do input
    const dataInput = document.getElementById('data_consulta');
    if (dataInput) {
        dataInput.setAttribute('min', dataMinima);
        dataInput.setAttribute('max', dataMaxima);
    } else {
        console.warn("Elemento 'data_consulta' não encontrado.");
    }
}

function limitarNumero() {
    const inputNumero = document.getElementById('telefone');
    if (inputNumero) {
        inputNumero.setAttribute('maxlength', '11');
        inputNumero.addEventListener('input', function () {
            // Remove qualquer caractere não numérico
            this.value = this.value.replace(/\D/g, '');
            // Limita o número a 11 caracteres
            if (this.value.length > 11) {
                this.value = this.value.slice(0, 11);
            }
        });
    } else {
        console.warn("Elemento 'telefone' não encontrado.");
    }
}

// Chama as funções ao carregar a página
window.onload = function() {
    generateTimeOptions();
    definirIntervaloData();
    atualizarDataFormatada(); // Chama para formatar a data ao carregar a página
    limitarNumero(); // Limita o número a 11 caracteres
};
