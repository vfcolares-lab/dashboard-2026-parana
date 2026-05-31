# 🎯 Dashboard Eleitoral Paraná 2026

## Análise Estratégica: Gleisi Hoffmann + Contexto Presidencial

---

## 📊 **O Dashboard em 3 Pontos**

### 1️⃣ **399 Municípios de Paraná**
- ✅ Dados eleitorais completos (2010-2022)
- ✅ Georreferenciados com coordenadas reais
- ✅ Análise histórica de 4 eleições

### 2️⃣ **Gleisi Hoffmann em 4 Eleições**
- 2010: **Senadora** (37.5% média)
- 2014: **Governadora** (queda para 18.6%)
- 2018: **Deputada Federal** (4.0%)
- 2022: **Deputada Federal** (2.9%)

### 3️⃣ **Contexto Presidencial (PT vs Bolsonaro)**
- Classificação por **MARGEM** (PT% - Bolsonaro%)
- 5 categorias: Bastião Petista → Tendência → Swing → Tendência Bolsonarista → Bastião
- Base para entender "piso" de Gleisi em cada município

---

## 🚀 **Como Usar**

### Local (recomendado para teste)
```bash
cd /Users/vitorcolares/Desktop/dashboard-2026-parana
python3 -m http.server 8001
```

Abra no navegador: **http://localhost:8001**

### Vercel (online, sempre disponível)
```
https://dashboard-2026-parana.vercel.app
```

---

## 🎛️ **6 Seções do Dashboard**

| Seção | O que você vê | Para quê |
|-------|---|---|
| **📌 Overview** | KPIs + Mapa + Scatter | Panorama geral em 1 tela |
| **📍 Municípios** | Tabela de 399 com filtros | Detalhe município por município |
| **📊 Classificação** | Distribuição federal 5 categorias | Entender base presidencial |
| **🎯 Preditivo** | Quadrantes Gleisi 2026 | Onde Gleisi é forte/fraca |
| **💥 Impulsionamento** | Seções eleitorais no mapa | Detalhe geográfico fino |
| **📋 Dados Brutos** | Exportar tudo | Excel/análise própria |

---

## 📈 **Distribuição Gleisi 2022**

**Preditivo 2026** (quintis de 80 municípios):

```
🟢 SEGURO GLEISI           80 municípios (20%)
🟠 COMPETITIVO PRÓ-GLEISI   80 municípios (20%)
🟡 BATTLEGROUND            80 municípios (20%)
🔴 COMPETITIVO CONTRA      80 municípios (20%)
⚫ DIFÍCIL                  79 municípios (20%)
```

---

## 📍 **Distribuição Federal 2022 (PT vs Bolsonaro)**

```
Bastião Bolsonarista     219 (54.9%) 🔴
Bastião Petista           69 (17.3%) 🟢
Swing                     53 (13.3%) 🟡
Tendência Bolsonarista    30 (7.5%)  🟠
Tendência Petista         28 (7.0%)  🟠
```

---

## 📂 **Arquivos Principais**

### `data.js` (576 KB)
Estrutura JSON com 399 municípios:
```json
{
  "municipio": "NOME",
  "presidencial": {
    "2010": { "pt_pct": 42.5, "oposicao_pct": 55.2, "margem": -12.7, "vencedor": "OPOSIÇÃO" },
    "2014": {...},
    "2018": {...},
    "2022": {...}
  },
  "gleisi": {
    "2010": 37.50,
    "2014": 18.58,
    "2018": 4.21,
    "2022": 2.93
  },
  "historico_federal": [
    { "ano": "2010", "classificacao": "Tendência Bolsonarista", "margem": -12.7 },
    { "ano": "2014", "classificacao": "Tendência Bolsonarista", "margem": -8.5 },
    { "ano": "2018", "classificacao": "Bastião Bolsonarista", "margem": -25.2 },
    { "ano": "2022", "classificacao": "Bastião Bolsonarista", "margem": -20.0 }
  ],
  "classificacao_2022": "Bastião Bolsonarista"
}
```

### `coords.json` (16 KB)
Latitude/longitude de cada município:
```json
{
  "CURITIBA": [-25.4284, -49.2733],
  "ABATIÁ": [-24.91, -50.6],
  ...
  "ÂNGULO": [-25.36, -51.48]
}
```

### `secoes_2022.json` (10.7 MB)
Votação por seção eleitoral (para "Impulsionamento"):
```json
{
  "MUNICIPIO": [
    { "secao": 1, "lat": -25.4, "lng": -49.2, "votos_pt": 234, "votos_bolso": 156 },
    ...
  ]
}
```

---

## 🔍 **Como Interpretar os Dados**

### Margem Presidencial
- `margem = PT% - Bolsonaro%`
- `> +10`: Bastião Petista (base PT forte)
- `+5 a +10`: Tendência Petista (PT na frente)
- `-5 a +5`: Swing (equilibrado)
- `-10 a -5`: Tendência Bolsonarista (Bolso frente)
- `< -10`: Bastião Bolsonarista (base Bolso forte)

### Gleisi vs Federal
- Se Gleisi % é **maior** que PT%, ela é **pessoalmente forte** lá
- Se Gleisi % é **menor** que PT%, ela está em **desvantagem pessoal**
- Exemplo:
  - ABATIÁ: PT 2022 = 35.4%, Gleisi = 2.3% → Gleisi 33pp abaixo (muito difícil)
  - ADRIANÓPOLIS: PT 2022 = 61.4%, Gleisi = 2.4% → Gleisi 59pp abaixo (muito difícil)

---

## 🧪 **Testes de Validação**

Execute um dos testes para verificar:

```bash
# Verificar que 399 municípios estão carregados
http://localhost:8001/test_399.html

# Testar mapa com 399 marcadores coloridos
http://localhost:8001/test_map.html

# Acompanhar status de carregamento (SECOES_2022 grande)
http://localhost:8001/test_loading.html
```

---

## ✅ **Checklist de Deploy**

- ✅ 399 municípios em data.js
- ✅ 399 coordenadas em coords.json
- ✅ Mapa Leaflet funcionando
- ✅ Scatter chart com 399 pontos
- ✅ Sem erros JavaScript
- ✅ MUNICIPIOS_COORDS carregando
- ✅ SECOES_2022 carregando
- ✅ Responsivo (desktop/tablet/mobile)
- ✅ Dark mode padrão
- ✅ Pronto para Vercel

---

## 🚀 **Deploy no Vercel**

1. **Conecte o repositório** ao Vercel
2. **Defina as variáveis** (se necessário)
3. **Deploy**: Vercel detecta `index.html` automaticamente
4. **URL públic**a: https://dashboard-2026-parana.vercel.app

### Configuração Recomendada
```json
{
  "buildCommand": "echo 'No build needed'",
  "outputDirectory": ".",
  "installCommand": "echo 'No dependencies'"
}
```

---

## 📞 **Suporte / Debug**

Se algo não funcionar:

1. **Abra DevTools** (F12)
2. **Vá para Console**
3. **Procure por ❌ erros vermelhos**
4. **Verifique Network**: coords.json e data.js carregaram?
5. **Teste direto**: `window.DASHBOARD_DATA` ou `window.MUNICIPIOS_COORDS`

---

## 📝 **Notas Técnicas**

- **Browser**: Chrome 90+, Firefox 88+, Safari 14+
- **Dados**: Atualizados até 30/05/2026
- **Versão**: 4.0-completo
- **Licença**: Dados públicos (TSE)
- **Desenvolvido com**: Chart.js, Leaflet.js, Pure JavaScript

---

**Última atualização**: 2026-05-30 22:30  
**Status**: ✅ Pronto para Produção
