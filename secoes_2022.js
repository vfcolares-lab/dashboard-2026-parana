// Carregar secoes_2022.json dinamicamente (arquivo grande: 10.7 MB)
console.log('📍 Iniciando fetch de secoes_2022.json (10.7 MB)...');
const startTime = Date.now();

fetch('secoes_2022.json')
    .then(response => {
        console.log(`📊 Response recebido em ${Date.now() - startTime}ms, size: ${response.headers.get('content-length')} bytes`);
        return response.json();
    })
    .then(data => {
        const elapsed = Date.now() - startTime;
        window.SECOES_2022 = data;
        const numMunics = Object.keys(data).length;
        console.log(`✅ SECOES_2022 carregado em ${elapsed}ms: ${numMunics} municípios com dados de seções`);
    })
    .catch(err => {
        console.error(`❌ Erro ao carregar secoes_2022.json após ${Date.now() - startTime}ms:`, err);
        console.error(`   Tipo: ${err.name}, Mensagem: ${err.message}`);
    });
