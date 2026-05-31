# 🚀 Guia Rápido - Dashboard Paraná 2026

## 🌍 Acessar o Dashboard

**URL**: https://dashboard-2026-parana.vercel.app

Abra no navegador. Sem necessidade de instalar nada ou deixar computador ligado.

---

## 📊 O que o Dashboard Mostra

### 1. **Dados Históricos de Gleisi**
- **2010**: Senadora (29.50% - seu melhor desempenho)
- **2014**: Governadora (14.87%)
- **2018**: Deputada Federal (3.71%)
- **2022**: Deputada Federal (4.26%)

### 2. **Classificação de Municípios (2022)**

#### 🟢 **Seguro Gleisi** (55 municípios - 13.8%)
- Gleisi acima da média estadual
- Votos tradicionais dela
- Estratégia: **Consolidar** base existente

#### 🟡 **Swing** (290 municípios - 72.7%)
- Equilibrado, pode ir para qualquer lado
- Maior oportunidade de crescimento
- Estratégia: **Impulsionamento concentrado**

#### 🔴 **Difícil Gleisi** (54 municípios - 13.5%)
- Gleisi abaixo da média
- Resistência local
- Estratégia: **Investimento alto** ou **focus em outros**

---

## 🔍 Como Usar

### Via Dashboard Online

1. Acesse: https://dashboard-2026-parana.vercel.app
2. Veja a tabela com todos os 399 municípios
3. Identifique a classificação de cada um
4. Veja os votos de 2010-2022

### Dados Disponíveis por Município

- **Gleisi % 2010**: Como ela foi na eleição de senadora
- **Gleisi % 2014**: Como ela foi na eleição de governadora
- **Gleisi % 2018**: Como ela foi na eleição de deputada (primeiro mandato)
- **Gleisi % 2022**: Como ela foi na reeleição
- **Índice**: Quanto acima (+) ou abaixo (-) da média estadual
- **Trajetória**: Se subiu ou caiu desde 2010

---

## 📈 Análise Estratégica

### Insight Principal

A votação de Gleisi **caiu drasticamente** de 2010 (29.50%) para 2022 (4.26%).

**Por quê?**
1. Em 2010 era eleição de senadora (2 vagas)
2. Em 2014 era governadora (1 vaga - maior visibilidade)
3. De 2018 em diante: deputada federal (menos visível)

### Oportunidades

**Em Swing (290 municípios)**:
- Teste de diferentes mensagens
- Maior ROI de campanha
- Onde a votação pode mudar

**Em Seguro Gleisi (55 municípios)**:
- Base consolidada
- Garantir mobilização
- Reforçar marca

**Em Difícil Gleisi (54 municípios)**:
- Decisão estratégica: investir ou ceder
- Se investir: mensagem diferenciada necessária

---

## 📥 Exportar Dados

(Função implementada no dashboard - clique em "Baixar CSV")

Coluna | Significado
------|--------
`municipio` | Nome do município
`gleisi_pct_2010` | % de votos para Gleisi em 2010
`gleisi_index_2010` | Índice em 2010 (+ acima da média)
`gleisi_pct_2022` | % de votos para Gleisi em 2022
`gleisi_classification` | Seguro / Swing / Difícil
`trajetoria` | Crescente / Decrescente / Estável

---

## 🔄 Atualizar os Dados

Se você receber novos dados de votação:

```bash
cd /Users/vitorcolares/Desktop/dashboard-2026-parana
python3 scripts/generate_dashboard_v2.py
git add data.js
git commit -m "Atualizar dados"
git push origin main
# O Vercel faz deploy automaticamente
```

---

## ❓ FAQ

**P: Por que aparece apenas Gleisi e não Lula/Bolsonaro?**
R: Os dados por seção do TSE não incluem eleições presidenciais. Estamos analisando a base específica de Gleisi.

**P: Posso ver dados de seções (não apenas municípios)?**
R: Sim, os dados por seção estão em `secoes_2022.json` para 2022.

**P: Como eu comparo com Amazonas?**
R: O dashboard do Amazonas tem Eduardo Braga (+2 candidatos). Este de Paraná tem apenas Gleisi.

---

## 📞 Suporte

Arquivo de dados: `/Users/vitorcolares/Desktop/dashboard-2026-parana/data.js`  
Script de processamento: `/Users/vitorcolares/Desktop/dashboard-2026-parana/scripts/generate_dashboard_v2.py`  
Repositório Git: `https://github.com/vfcolares-lab/dashboard-2026-parana`

---

**Status**: ✅ Pronto para uso  
**Versão**: 2.0-gleisi  
**Data**: 30 de maio de 2026
