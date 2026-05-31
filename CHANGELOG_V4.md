# 📊 Dashboard V4 - Classificação por MARGEM

## 🔄 **O Que Mudou**

### ❌ **REMOVIDO (V3 - Arbitrário)**
```python
# Antes: Classificação por índice estadual
if pt_index > 5:  # 5 pontos acima da média
    class = 'Bastião Petista'
```
**Problema**: Arbitrário e sem fundamentação estratégica

---

### ✅ **NOVO (V4 - Por MARGEM)**
```python
margem = PT% - Bolsonaro%

if margem > 10:
    class = 'Bastião Petista'        # PT venceu forte
elif margem >= 5:
    class = 'Tendência Petista'      # PT venceu leve
elif margem > -5:
    class = 'Swing'                  # Equilibrado
elif margem >= -10:
    class = 'Tendência Bolsonarista' # Bolsonaro venceu leve
else:
    class = 'Bastião Bolsonarista'   # Bolsonaro venceu forte
```

---

## 📊 **Resultados 2022 - REAL**

| Classificação | Municípios | % | Situação |
|---|---|---|---|
| 🔴 Bastião Bolsonarista | **219** | **54.9%** | Bolsonaro domina |
| 🟢 Bastião Petista | **69** | **17.3%** | PT tem base |
| 🟡 Swing | **53** | **13.3%** | Equilibrado |
| 🟠 Tendência Bolsonarista | **30** | **7.5%** | Bolsonaro na frente |
| 🟠 Tendência Petista | **28** | **7.0%** | PT na frente |

**Interpretação**:
- Bolsonaro venceu em **62.4%** dos municípios (219 + 30)
- PT venceu em **24.3%** dos municípios (69 + 28)
- **13.3%** foi muito equilibrado

---

## 📈 **Estrutura de Dados - Cada Município**

```json
{
  "ABATIÁ": {
    "municipio": "ABATIÁ",
    "presidencial": {
      "2010": {
        "pt_pct": 44.34,
        "oposicao_pct": 52.36,
        "margem": -8.02,           // PT - Oposição
        "vencedor": "OPOSIÇÃO"
      },
      "2014": {...},
      "2018": {...},
      "2022": {
        "pt_pct": 35.42,
        "oposicao_pct": 61.17,
        "margem": -25.75,          // Bolsonaro venceu por 25.75pp
        "vencedor": "OPOSIÇÃO"
      }
    },
    "gleisi": {
      "2010": 37.50,   // Senadora
      "2014": 12.41,   // Governadora
      "2018": 4.20,    // Deputada
      "2022": 2.58     // Deputada
    },
    "historico_federal": [
      { "ano": "2010", "classificacao": "Tendência Bolsonarista", "margem": -8.02 },
      { "ano": "2014", "classificacao": "Bastião Bolsonarista", "margem": -12.21 },
      { "ano": "2018", "classificacao": "Bastião Bolsonarista", "margem": -21.13 },
      { "ano": "2022", "classificacao": "Bastião Bolsonarista", "margem": -25.75 }
    ],
    "classificacao_2022": "Bastião Bolsonarista"
  }
}
```

---

## 🎯 **Insights com a V4**

### **Trajetória Histórica**
Cada município mostra como evoluiu de 2010-2022:
- Se foi sempre Bastião Petista → Base consolidada
- Se foi Swing em alguns anos → Volatilidade
- Se virou Bastião Bolsonarista → Perda de apoio

### **ABATIÁ (Exemplo)**
- 2010: Tendência Bolsonarista (-8pp)
- 2014: Bastião Bolsonarista (-12pp)
- 2018: Bastião Bolsonarista (-21pp)
- 2022: Bastião Bolsonarista (-26pp) ← **Piora contínua**

### **Gleisi em ABATIÁ**
- Senadora 2010: 37.50% (seu melhor em Abatiá)
- Governadora 2014: 12.41% (queda de 25pp)
- Deputada 2018: 4.20% (queda de 8pp)
- Deputada 2022: 2.58% (queda de 1.6pp)

**Conclusão**: Abatiá é uma "fortaleza bolsonarista" onde Gleisi perdeu força dramaticamente.

---

## 🔍 **Análises Possíveis com V4**

1. **Municípios que oscilam** (Swing em vários anos)
   - Maior ROI de campanha
   - Onde a mensagem pode impactar

2. **Municípios que consolidam** (sempre na mesma classificação)
   - Se é Bastião Petista: mobilizar
   - Se é Bastião Bolsonarista: talvez ceder

3. **Municípios que mudam** (era Petista, ficou Bolsonarista)
   - Entender por que perdeu apoio
   - Recuperar ou aceitar?

4. **Gleisi em contraste**
   - Em Bastião Petista, Gleisi tem % melhor?
   - Em Bastião Bolsonarista, Gleisi é "ponte"?

---

## 🚀 **Deploy**

**Status**: ✅ Online no Vercel  
**URL**: https://dashboard-2026-parana.vercel.app  
**Versão**: 4.0-margem  
**Data**: 30 de maio de 2026

---

## 📝 **Diferenças V3 → V4**

| Aspecto | V3 | V4 |
|---------|----|----|
| **Lógica** | Índice estatal (arbitrário) | Margem PT - Bolsonaro (estratégico) |
| **Clareza** | Confuso (5pp acima de quê?) | Claro (PT venceu por >10pp) |
| **Histórico** | Sem trajetória | ✅ Mostra 2010-2022 |
| **Gleisi** | Misturada com presidencial | ✅ Separada e clara |
| **Realismo** | 50% Bastião Petista | ✅ 54.9% Bastião Bolsonarista |

---

**V4 é muito mais estratégica e realista!** 🎯
