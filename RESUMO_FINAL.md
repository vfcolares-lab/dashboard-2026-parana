# 🎯 Dashboard Eleitoral Paraná 2026 - RESUMO FINAL ✅

## 🌍 **Acesso**
### **https://dashboard-2026-parana.vercel.app**

---

## 📊 **Dados Integrados (COMPLETO)**

### **Eleições Presidenciais (4 eleições)**

| Ano | PT | Oposição | Vencedor | Seções |
|-----|----|---------|----|--------|
| **2010** | Dilma 41.72% | Serra 49.63% | 🔵 Oposição | 17,668 |
| **2014** | Dilma 35.79% | Aécio 55.45% | 🔵 Oposição | 19,154 |
| **2018** | Haddad 25.65% | Bolsonaro 62.67% | 🔵 Oposição | 23,300 |
| **2022** | Lula 36.80% | Bolsonaro 58.85% | 🔵 Oposição | 23,862 |

### **Candidatura de Gleisi (4 eleições)**

| Ano | Cargo | Votação Gleisi | Seções |
|-----|-------|-----------------|--------|
| **2010** | Senadora | 29.50% | 17,668 |
| **2014** | Governadora | 14.87% | 19,154 |
| **2018** | Deputada Federal | 3.71% | 23,300 |
| **2022** | Deputada Federal | 4.26% | 23,862 |

---

## 🏛️ **Classificação Federal - 2022 (Lula vs Bolsonaro)**

### Distribuição dos 399 Municípios:

```
🔴 Bastião Petista          201 (50.4%)  ← PT muito acima da média
🟠 Tendência Petista         90 (22.6%)  ← PT acima da média  
🟡 Swing                     42 (10.5%)  ← Equilibrado
🔵 Tendência Bolsonarista    66 (16.5%)  ← Bolsonaro acima da média
```

**Insight**: Paraná tem **maioria "Bastião Petista"** mas Bolsonaro venceu (58.85% vs 36.80%)

---

## 👩‍💼 **Classificação Gleisi - 2022**

### Distribuição dos 399 Municípios:

```
🟢 Seguro Gleisi        55 (13.8%)  ← Gleisi acima da média
🟡 Swing              290 (72.7%)  ← Equilibrado (maioria)
🔴 Difícil Gleisi       54 (13.5%)  ← Gleisi abaixo da média
```

**Insight**: Maioria dos municípios é "Swing" - oportunidade de crescimento

---

## 💡 **Análise Estratégica Bidimensional**

### Combinações Possíveis (Federal + Gleisi):

#### 🔴🟢 Bastião Petista + Seguro Gleisi
- Base tradicional forte
- Estratégia: **Consolidar e mobilizar**

#### 🔴🟡 Bastião Petista + Swing Gleisi
- PT forte mas Gleisi equilibrada
- Estratégia: **Fortalecer marca de Gleisi**

#### 🟡🟡 Swing Federal + Swing Gleisi
- Máxima volatilidade (290 + 290 = 580 pares possíveis)
- Estratégia: **Teste A/B de mensagens**

#### 🔵🔴 Tendência Bolsonarista + Difícil Gleisi
- Resistência dupla
- Estratégia: **Alto investimento ou ceder**

---

## 📈 **Trajetória (2010-2022)**

### **PT (Presidencial)**
```
2010: 41.72% (Dilma)
2014: 35.79% (Dilma)  ↓ -5.93pp
2018: 25.65% (Haddad) ↓ -10.14pp
2022: 36.80% (Lula)   ↑ +11.15pp
```
**Conclusão**: Oscilação forte, recuperação parcial em 2022

### **Gleisi (Candidata)**
```
2010: 29.50% (Senadora)
2014: 14.87% (Governadora) ↓ -14.63pp
2018: 3.71% (Deputada)     ↓ -11.16pp
2022: 4.26% (Deputada)     ↑ +0.55pp
```
**Conclusão**: Queda dramática de senadora (29.50%) para deputada (3.71%)

---

## 🎯 **Oportunidades Estratégicas**

### 1️⃣ **Municípios Swing (290)**
- Onde Gleisi pode crescer mais
- Maior ROI de campanha
- Testar diferentes mensagens

### 2️⃣ **Bastião Petista (201)**
- Base consolidada
- Garantir mobilização
- Reforçar marca de Gleisi nestes

### 3️⃣ **Difícil Gleisi (54)**
- Decisão estratégica: investir ou ceder?
- Se investir: mensagem diferenciada

---

## 📁 **Arquivos & Links**

| Recurso | Link |
|---------|------|
| **Dashboard Online** | https://dashboard-2026-parana.vercel.app |
| **GitHub** | https://github.com/vfcolares-lab/dashboard-2026-parana |
| **Dados (JavaScript)** | `data.js` (278 KB) |
| **Dados (JSON)** | `data/dashboard_2026_completo.json` |
| **Script** | `scripts/generate_dashboard_completo.py` |

---

## 🚀 **Como Usar**

### **Online (Sem Instalar Nada)**
1. Acesse: https://dashboard-2026-parana.vercel.app
2. Navegue pelos 399 municípios
3. Veja classificação federal e de Gleisi
4. Exporte dados em CSV (botão disponível)

### **Atualizar com Novos Dados**
```bash
cd /Users/vitorcolares/Desktop/dashboard-2026-parana
python3 scripts/generate_dashboard_completo.py
git add data.js
git commit -m "Update: novos dados"
git push origin main
# Vercel faz deploy automático em ~30 segundos
```

---

## ✨ **Status Final**

| Aspecto | Status |
|---------|--------|
| **Dados Presidenciais (4 anos)** | ✅ COMPLETO |
| **Dados de Gleisi (4 anos)** | ✅ COMPLETO |
| **Municípios Mapeados** | ✅ 399/399 |
| **Seções Analisadas** | ✅ ~23,000 (2022) |
| **Análise Bidimensional** | ✅ IMPLEMENTADA |
| **Dashboard Online** | ✅ PRONTO |
| **Sem Depender de Computador Local** | ✅ SIM (Vercel) |

---

## 🎓 **Próximos Passos Opcionais**

1. **Integrar dados de outras candidaturas** (Lula, Bolsonaro, outros candidatos)
2. **Análise por zona eleitoral** (mais granular que município)
3. **Dashboard de acompanhamento em tempo real** (durante campanha 2026)
4. **Comparação com Amazonas** (outro dashboard de Eduardo Braga)
5. **Projeções** (baseadas em volatilidade e tendências)

---

**Dashboard criado com sucesso!**  
**Versão**: 3.0-completo  
**Data**: 30 de maio de 2026  
**Criado por**: Claude + Vitor Colares  
**Status**: ✅ Produção
