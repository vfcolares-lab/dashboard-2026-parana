# 📋 PLANO EXECUTIVO: DASHBOARD ELEITORAL PARANÁ 2026
## Gleisi Hoffmann + PT Presidencial

---

## 1. METODOLOGIA DE ANÁLISE

### 1.1 Ajuste de Votos (Comparabilidade)
```
2010 (Senado - 2 votos): Dividir por 2
2014 (Governadora - 1 voto): Usar como base
2018 (Deputada - 1 voto): Usar como base
2022 (Deputada - 1 voto): Usar como base

Fórmula: votos_2010_ajustados = votos_2010_brutos / 2
```

### 1.2 Períodos de Comparação
```
PERÍODO 1: 2010 vs 2014 (Gleisi Majoritária)
- Eleição de Senado vs Governadora
- Análise: Margem, crescimento/queda por município

PERÍODO 2: 2018 vs 2022 (Gleisi Proporcional)
- Eleição de Deputada Federal
- Análise: Votos diretos, volatilidade
```

### 1.3 Índices a Calcular

#### **Índice Gleisi (IG)**
```
IG = (% votos Gleisi na seção - % votos Gleisi no estado) / 100

Positivo: Seção acima da média de Gleisi
Negativo: Seção abaixo da média de Gleisi
```

#### **Índice PT Presidencial (IPT)**
```
Para 2010-2014:
IPT_2010_2014 = (% Dilma 2010 - % Dilma 2014) na seção

Para 2018-2022:
IPT_2018_2022 = (% Lula 2022 - % Haddad 2018) na seção

Mede: Oscilação entre eleições
```

#### **Índice de Correlação Gleisi-PT (ICC)**
```
ICC = IG + IPT (normalizados)

Indica: Se Gleisi cresce quando PT cresce
```

---

## 2. CATEGORIZAÇÃO DE SEÇÕES

### Baseado em 3 eixos:
```
1. FORÇA DE GLEISI (IG)
   - Bastião Gleisi: IG > +0.10
   - Favorável: IG +0.03 a +0.10
   - Swing: IG -0.03 a +0.03
   - Desfavorável: IG -0.05 a -0.03
   - Difícil: IG < -0.05

2. DESEMPENHO PT (IPT)
   - PT em alta: IPT > +0.10
   - PT estável: IPT -0.10 a +0.10
   - PT em queda: IPT < -0.10

3. CORRELAÇÃO GLEISI-PT (ICC)
   - Muito correlacionada
   - Fracamente correlacionada
   - Independente
```

### 5 Categorias Finais:
```
🟢 BASTIÃO GLEISI-PT
   - Alto desempenho Gleisi + PT forte
   - Prioridade: Consolidar

🟦 GLEISI CRESCENTE
   - Gleisi forte + PT em alta
   - Prioridade: Reforçar marca

🟡 SWING GLEISI-PT
   - Oscilante em ambos
   - Prioridade: Máxima atenção

🟠 GLEISI FRÁGIL + PT FRACO
   - Baixo desempenho em ambos
   - Prioridade: Investimento alto

🔴 DIFÍCIL GLEISI-PT
   - Muito desfavorável
   - Prioridade: Tática defensiva
```

---

## 3. ESTRUTURA DE DADOS POR SEÇÃO

```json
{
  "numero_secao": 1,
  "municipio": "CURITIBA",
  "endereco": "RUA X, SN",
  "latitude": -25.4244,
  "longitude": -49.2645,
  "raio_km": 3.5,
  
  "historico": {
    "2010": {
      "presidente": "DILMA",
      "candidata": "GLEISI",
      "cargo": "SENADO",
      "votos_gleisi": 450,
      "votos_gleisi_ajustado": 225,
      "votos_dilma": 520,
      "pct_gleisi": 45.2,
      "pct_dilma": 52.1
    },
    "2014": {...},
    "2018": {...},
    "2022": {...}
  },
  
  "indices": {
    "ig_2010_2014": 0.054,
    "ig_2018_2022": 0.089,
    "ipt_2010_2014": -0.023,
    "ipt_2018_2022": 0.142,
    "icc_geral": 0.087,
    "volatilidade": 0.15,
    "tendencia": "positiva"
  },
  
  "categorias": {
    "2010_2014": "GLEISI_CRESCENTE",
    "2018_2022": "BASTIAO_GLEISI_PT",
    "geral_2026": "BASTIAO_GLEISI_PT"
  },
  
  "preditivo_2026": {
    "cargo": "SENADO",
    "vagas": 2,
    "cenario_base": {
      "gleisi_projecao_pct": 38.5,
      "lula_projecao_pct": 51.2,
      "margem_gleisi": 0.156
    },
    "cenario_otimista": {
      "gleisi_projecao_pct": 42.3,
      "lula_projecao_pct": 54.1
    },
    "cenario_pessimista": {
      "gleisi_projecao_pct": 34.7,
      "lula_projecao_pct": 48.3
    },
    "probabilidade_eleicao": 0.82,
    "tipo_conteudo_sugerido": "CONSOLIDAÇÃO",
    "tom_recomendado": "REFORÇO DE MARCA"
  },
  
  "impulsionamento": {
    "prioridade": 1,
    "tipo_conteudo": ["GESTÃO", "SENADORA", "LULA", "PROGRAMAS SOCIAIS"],
    "plataforma_recomendada": ["FACEBOOK", "WHATSAPP"],
    "budget_sugerido": "ALTO",
    "densidade_secao": "alta"
  }
}
```

---

## 4. FUNCIONALIDADES DO DASHBOARD

### 4.1 Mapa Interativo
- ✅ Visualizar 20.232 seções por categoria
- ✅ Filtrar por município (399 municípios)
- ✅ Zoom automático
- ✅ Hover mostra: número, endereço, categoria, votos 2022

### 4.2 Aba "Radar Eleitoral Gleisi-PT"
- Índice Gleisi por município
- Índice PT por município
- Correlação Gleisi-PT
- Ranking: Mais favoráveis vs Mais desfavoráveis
- Evolução 2010→2014 vs 2018→2022

### 4.3 Aba "Impulsionamento"
- Seletor de município
- Mapa com todas as seções
- Cores por categoria
- **CSV Download com:**
  - numero_secao
  - municipio
  - endereco
  - latitude, longitude, raio_km
  - categoria
  - indices (IG, IPT, ICC)
  - tipo_conteudo_sugerido
  - prioridade_impulsionamento

### 4.4 Aba "Análise Histórica"
- Gráficos: Gleisi 2010 vs 2014 vs 2018 vs 2022
- Gráficos: PT Presidencial (Dilma → Haddad → Lula)
- Tabela: Municípios ordenados por desempenho

### 4.5 Aba "Preditivo 2026"
- Projeção por município
- Cenários (base, otimista, pessimista)
- Probabilidade de eleição (2 vagas)
- Recomendações de conteúdo

### 4.6 Aba "Dados Brutos"
- Tabela com 20.232 seções
- Busca por município
- Download CSV/XML/JSON

---

## 5. CÁLCULO DO RAIO DE IMPULSIONAMENTO

```python
# Densidade de seções por município
densidade = total_secoes_municipio / area_municipio

if densidade > 50 seções/km²:
    raio = 3.0  # Alta densidade (ex: Curitiba)
elif densidade > 20:
    raio = 5.0  # Média densidade
elif densidade > 5:
    raio = 7.0  # Baixa densidade
else:
    raio = 10.0  # Muito baixa densidade (interior)
```

---

## 6. ROTEIRO DE IMPLEMENTAÇÃO

### Fase 1: Preparação de Dados (2 horas)
- [ ] Carregar 4 arquivos TSE (2010, 2014, 2018, 2022)
- [ ] Ajustar votos 2010 (dividir por 2)
- [ ] Normalizar nomes (Gleisi, Dilma, Haddad, Lula)
- [ ] Filtrar dados do Paraná

### Fase 2: Processamento e Cálculo (3 horas)
- [ ] Calcular IG, IPT, ICC para cada seção
- [ ] Categorizar 20.232 seções
- [ ] Gerar coordenadas com raio variável
- [ ] Calcular preditivo 2026

### Fase 3: Frontend e Deploy (3 horas)
- [ ] Adaptar index.html para PR
- [ ] Gerar dados JSON
- [ ] Testar localamente
- [ ] Deploy Vercel

**Total: ~8 horas**

---

## 7. REPOSITÓRIO

```
Nome: dashboard-2026-parana
ou
dashboard-2026 (branch: parana)

Estrutura:
/parana/
  index.html
  secoes_2022.json
  secoes_2022.js
  TODAS_SECOES_MAPEADAS.csv
  TODAS_SECOES_MAPEADAS.xml
  recalculate_sections_pr.py
  add_coordinates_pr.py
```

---

## 8. PROTOTIPAGEM DE CONTEÚDO

**Exemplo: Seção em Curitiba (Bastião Gleisi-PT)**
```
Categoria: BASTIÃO GLEISI-PT
Tipo de conteúdo: CONSOLIDAÇÃO
Sugestões:
- ✅ Reforçar: "Gleisi Senadora"
- ✅ Ligar com: Lula Presidente
- ✅ Programas: Sociais (pensão, auxílio)
- ✅ Tom: Confiança, continuidade
- ❌ NÃO usar: Confronto, crítica
```

**Exemplo: Seção no Interior (Swing Gleisi-PT)**
```
Categoria: SWING GLEISI-PT
Tipo de conteúdo: PERSUASÃO
Sugestões:
- ✅ Foco: Mudança positiva
- ✅ Ligar com: Gestão + Lula
- ✅ Programas: Infraestrutura (BR, pontes, estradas)
- ✅ Tom: Esperança, crescimento
- ❌ NÃO usar: Demagogia excessiva
```

---

**Status:** 🚀 Pronto para começar!
