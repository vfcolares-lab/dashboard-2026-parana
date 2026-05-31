#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate complete dashboard data for Paraná 2026 with 4-year presidential history
Analyzes:
- Presidential elections: PT (Lula/Haddad) vs Bolsonaro (2010-2022)
- Gleisi candidacies: Senado 2010, Governador 2014, Deputada Federal 2018/2022
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

BASE_PATH = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/raw')
OUTPUT_DIR = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana')

print("=" * 80)
print("GERANDO DADOS COMPLETOS DO DASHBOARD PARANÁ 2026")
print("=" * 80)

# ===========================================================================
# LOAD ELECTORAL DATA FOR ALL 4 YEARS
# ===========================================================================

print("\n📥 Carregando dados eleitorais...")

dfs = {}
for year in [2010, 2014, 2018, 2022]:
    try:
        df = pd.read_csv(
            BASE_PATH / f'votacao_secao_{year}_PR.csv',
            delimiter=';',
            encoding='latin-1',
            low_memory=False
        )
        df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip().str.upper()
        df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
        df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()
        dfs[year] = df
        print(f"  ✓ {year}: {len(df):,} registros")
    except Exception as e:
        print(f"  ✗ {year}: {e}")
        dfs[year] = pd.DataFrame()

# ===========================================================================
# EXTRACT PRESIDENTIAL DATA (PT vs BOLSONARO)
# ===========================================================================

print("\n🗳️  Extraindo dados presidenciais...")

presidential_data = {}

# 2010: Presidential election
print("  2010: Presidente")
df_pres_2010 = dfs[2010][dfs[2010]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
if len(df_pres_2010) > 0:
    pres_2010_agg = {}
    for (mun, secao), group in df_pres_2010.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        lula = group[group['NM_VOTAVEL'].str.contains('LULA|SERRA', case=False, na=False)]['QT_VOTOS'].sum()
        # 2010: Lula vs Serra
        serra = group[group['NM_VOTAVEL'].str.contains('SERRA', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in presidential_data:
            presidential_data[(mun, secao)] = {}
        presidential_data[(mun, secao)]['2010'] = {
            'pt': int(lula),
            'oposicao': int(serra),
            'total': int(total)
        }
    print(f"    ✓ {len(pres_2010_agg):,} seções")

# 2014: Presidential election
print("  2014: Presidente")
df_pres_2014 = dfs[2014][dfs[2014]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
if len(df_pres_2014) > 0:
    for (mun, secao), group in df_pres_2014.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        dilma = group[group['NM_VOTAVEL'].str.contains('DILMA', case=False, na=False)]['QT_VOTOS'].sum()
        aecio = group[group['NM_VOTAVEL'].str.contains('AÉCIO|AECIO', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in presidential_data:
            presidential_data[(mun, secao)] = {}
        presidential_data[(mun, secao)]['2014'] = {
            'pt': int(dilma),
            'oposicao': int(aecio),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in presidential_data.keys()]):,} seções")

# 2018: Presidential election
print("  2018: Presidente")
df_pres_2018 = dfs[2018][dfs[2018]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
if len(df_pres_2018) > 0:
    for (mun, secao), group in df_pres_2018.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        pt = group[group['NM_VOTAVEL'].str.contains('HADDAD|PT', case=False, na=False)]['QT_VOTOS'].sum()
        bolsonaro = group[group['NM_VOTAVEL'].str.contains('BOLSONARO', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in presidential_data:
            presidential_data[(mun, secao)] = {}
        presidential_data[(mun, secao)]['2018'] = {
            'pt': int(pt),
            'oposicao': int(bolsonaro),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in presidential_data.keys()]):,} seções")

# 2022: Presidential election
print("  2022: Presidente")
df_pres_2022 = dfs[2022][dfs[2022]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
if len(df_pres_2022) > 0:
    for (mun, secao), group in df_pres_2022.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        lula = group[group['NM_VOTAVEL'].str.contains('LULA|PT', case=False, na=False)]['QT_VOTOS'].sum()
        bolsonaro = group[group['NM_VOTAVEL'].str.contains('BOLSONARO', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in presidential_data:
            presidential_data[(mun, secao)] = {}
        presidential_data[(mun, secao)]['2022'] = {
            'pt': int(lula),
            'oposicao': int(bolsonaro),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in presidential_data.keys()]):,} seções")

# ===========================================================================
# EXTRACT GLEISI DATA
# ===========================================================================

print("\n👩‍💼 Extraindo dados de Gleisi...")

gleisi_data = {}

# 2010: Senadora
print("  2010: Senadora")
df_sen_2010 = dfs[2010][dfs[2010]['DS_CARGO'].str.contains('SENADOR', na=False)].copy()
if len(df_sen_2010) > 0:
    for (mun, secao), group in df_sen_2010.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in gleisi_data:
            gleisi_data[(mun, secao)] = {}
        gleisi_data[(mun, secao)]['2010'] = {
            'votos': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ Senadora em {len(gleisi_data):,} seções")

# 2014: Governadora
print("  2014: Governadora")
df_gov_2014 = dfs[2014][dfs[2014]['DS_CARGO'].str.contains('GOVERNADOR', na=False)].copy()
if len(df_gov_2014) > 0:
    for (mun, secao), group in df_gov_2014.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in gleisi_data:
            gleisi_data[(mun, secao)] = {}
        gleisi_data[(mun, secao)]['2014'] = {
            'votos': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ Governadora em {len(gleisi_data):,} seções")

# 2018: Deputada Federal
print("  2018: Deputada Federal")
df_dep_2018 = dfs[2018][dfs[2018]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
if len(df_dep_2018) > 0:
    for (mun, secao), group in df_dep_2018.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in gleisi_data:
            gleisi_data[(mun, secao)] = {}
        gleisi_data[(mun, secao)]['2018'] = {
            'votos': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ Deputada Federal em {len(gleisi_data):,} seções")

# 2022: Deputada Federal
print("  2022: Deputada Federal")
df_dep_2022 = dfs[2022][dfs[2022]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
if len(df_dep_2022) > 0:
    for (mun, secao), group in df_dep_2022.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in gleisi_data:
            gleisi_data[(mun, secao)] = {}
        gleisi_data[(mun, secao)]['2022'] = {
            'votos': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ Deputada Federal em {len(gleisi_data):,} seções")

# ===========================================================================
# AGGREGATE BY MUNICIPALITY FOR STATE AVERAGES
# ===========================================================================

print("\n📊 Calculando médias estaduais...")

municipality_totals = defaultdict(lambda: {
    '2010': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
    '2014': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
    '2018': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
    '2022': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
})

# Aggregate presidential data by municipality
for (mun, secao), years in presidential_data.items():
    for year, data in years.items():
        municipality_totals[mun][year]['pt'] += data['pt']
        municipality_totals[mun][year]['oposicao'] += data['oposicao']
        municipality_totals[mun][year]['total'] += data['total']

# Aggregate Gleisi data by municipality
for (mun, secao), years in gleisi_data.items():
    for year, data in years.items():
        municipality_totals[mun][year]['gleisi'] += data['votos']
        municipality_totals[mun][year]['gleisi_total'] += data['total']

# Calculate state averages
state_averages = {}
for year in ['2010', '2014', '2018', '2022']:
    total_pt = sum(mun[year]['pt'] for mun in municipality_totals.values())
    total_oposicao = sum(mun[year]['oposicao'] for mun in municipality_totals.values())
    total_votos = sum(mun[year]['total'] for mun in municipality_totals.values())

    total_gleisi = sum(mun[year]['gleisi'] for mun in municipality_totals.values())
    total_gleisi_votos = sum(mun[year]['gleisi_total'] for mun in municipality_totals.values())

    state_averages[year] = {
        'pt_pct': (total_pt / total_votos * 100) if total_votos > 0 else 0,
        'oposicao_pct': (total_oposicao / total_votos * 100) if total_votos > 0 else 0,
        'gleisi_pct': (total_gleisi / total_gleisi_votos * 100) if total_gleisi_votos > 0 else 0,
    }

    print(f"  {year}:")
    print(f"    PT: {state_averages[year]['pt_pct']:.2f}%")
    print(f"    Oposição: {state_averages[year]['oposicao_pct']:.2f}%")
    print(f"    Gleisi: {state_averages[year]['gleisi_pct']:.2f}%")

# ===========================================================================
# BUILD MUNICIPAL CLASSIFICATION DATA
# ===========================================================================

print("\n🏛️  Classificando municípios...")

municipal_data = {}

for mun, years in sorted(municipality_totals.items()):
    # Calculate percentages and indices for each year
    mun_analysis = {
        'municipio': mun,
        'anos': {}
    }

    for year in ['2010', '2014', '2018', '2022']:
        year_data = years[year]

        pt_pct = (year_data['pt'] / year_data['total'] * 100) if year_data['total'] > 0 else 0
        oposicao_pct = (year_data['oposicao'] / year_data['total'] * 100) if year_data['total'] > 0 else 0
        gleisi_pct = (year_data['gleisi'] / year_data['gleisi_total'] * 100) if year_data['gleisi_total'] > 0 else 0

        # Federal indices (presidential)
        pt_index = pt_pct - state_averages[year]['pt_pct']
        oposicao_index = oposicao_pct - state_averages[year]['oposicao_pct']

        # Gleisi index
        gleisi_index = gleisi_pct - state_averages[year]['gleisi_pct']

        mun_analysis['anos'][year] = {
            'pt_pct': round(pt_pct, 2),
            'oposicao_pct': round(oposicao_pct, 2),
            'gleisi_pct': round(gleisi_pct, 2),
            'pt_index': round(pt_index, 3),
            'oposicao_index': round(oposicao_index, 3),
            'gleisi_index': round(gleisi_index, 3),
        }

    # Federal classification (2022 as primary)
    pt_index_2022 = mun_analysis['anos']['2022']['pt_index']
    oposicao_index_2022 = mun_analysis['anos']['2022']['oposicao_index']

    if pt_index_2022 > 5:
        federal_class = 'Bastião Petista'
    elif pt_index_2022 > 0:
        federal_class = 'Tendência Petista'
    elif abs(pt_index_2022) < 3:
        federal_class = 'Swing'
    elif oposicao_index_2022 > 0:
        federal_class = 'Tendência Bolsonarista'
    else:
        federal_class = 'Bastião Bolsonarista'

    mun_analysis['federal_classification'] = federal_class

    # Gleisi classification (2022 as primary)
    gleisi_index_2022 = mun_analysis['anos']['2022']['gleisi_index']

    if gleisi_index_2022 > 5:
        gleisi_class = 'Seguro Gleisi'
    elif gleisi_index_2022 > 0:
        gleisi_class = 'Dificil Gleisi'
    else:
        gleisi_class = 'Swing'

    mun_analysis['gleisi_classification'] = gleisi_class

    municipal_data[mun] = mun_analysis

print(f"  ✓ {len(municipal_data)} municípios classificados")

# ===========================================================================
# GENERATE DASHBOARD DATA STRUCTURE
# ===========================================================================

print("\n📈 Gerando estrutura final...")

# Count classifications
federal_counts = defaultdict(int)
gleisi_counts = defaultdict(int)

for mun, data in municipal_data.items():
    federal_counts[data['federal_classification']] += 1
    gleisi_counts[data['gleisi_classification']] += 1

dashboard_data = {
    'metadata': {
        'projeto': 'Dashboard Eleitoral Paraná 2026',
        'analise': 'Gleisi Hoffmann',
        'anos': [2010, 2014, 2018, 2022],
        'municipios_total': len(municipal_data),
        'data_geracao': '2026-05-30',
        'versao': '2.0',
    },
    'estado': {
        'media_estadual': state_averages,
        'municipios_count': len(municipal_data),
        'federal_distribution': dict(federal_counts),
        'gleisi_distribution': dict(gleisi_counts),
    },
    'municipios': municipal_data,
}

# ===========================================================================
# SAVE DATA
# ===========================================================================

print("\n💾 Salvando dados...")

# Save as JavaScript
with open(OUTPUT_DIR / 'data.js', 'w', encoding='utf-8') as f:
    f.write('const DASHBOARD_DATA = ')
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    f.write(';\n')

print(f"  ✓ data.js ({len(str(dashboard_data))} bytes)")

# Save as JSON for reference
with open(OUTPUT_DIR / 'data' / 'dashboard_2026.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"  ✓ data/dashboard_2026.json")

# ===========================================================================
# SUMMARY
# ===========================================================================

print("\n" + "=" * 80)
print("✅ DASHBOARD DATA GENERATION COMPLETO!")
print("=" * 80)

print("\n📊 RESUMO ESTADUAL (2022):")
print(f"  PT: {state_averages['2022']['pt_pct']:.2f}%")
print(f"  Oposição: {state_averages['2022']['oposicao_pct']:.2f}%")
print(f"  Gleisi: {state_averages['2022']['gleisi_pct']:.2f}%")

print("\n🏛️  CLASSIFICAÇÃO FEDERAL (Presidencial):")
for classification, count in sorted(federal_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(municipal_data) * 100)
    print(f"  {classification}: {count} municípios ({pct:.1f}%)")

print("\n👩‍💼 CLASSIFICAÇÃO GLEISI:")
for classification, count in sorted(gleisi_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(municipal_data) * 100)
    print(f"  {classification}: {count} municípios ({pct:.1f}%)")

print("\n✨ O dashboard está pronto para ser testado localmente!")
print("   Próximo passo: Testar em http://localhost:8001")
