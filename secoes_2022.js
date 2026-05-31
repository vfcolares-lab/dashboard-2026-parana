// Carregar secoes_2022.json dinamicamente
fetch('secoes_2022.json')
    .then(response => response.json())
    .then(data => {
        window.SECOES_2022 = data;
        console.log('✅ SECOES_2022 carregado:', Object.keys(data).length, 'municípios');
    })
    .catch(err => console.error('❌ Erro ao carregar secoes_2022.json:', err));
