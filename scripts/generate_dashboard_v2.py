#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate dashboard data for Paraná 2026 with Gleisi historical analysis
Uses: Senado 2010, Governador 2014, Deputada Federal 2018/2022
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

BASE_PATH = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/raw')
OUTPUT_DIR = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana')

print("=" * 80)
print("GERANDO DADOS PARANÁ 2026 - ANÁLISE GLEISI")
print("=" * 80)

# ===========================================================================
# LOAD DATA
# ===========================================================================

print("\n📥 Carregando dados...")

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
# EXTRACT GUBERNATORIAL & SENATORIAL DATA (as proxy for political alignment)
# ===========================================================================

print("\n🏛️  Extraindo dados políticos (Governador/Senador)...")

political_data = {}

# 2010: Senado (Gleisi concorreu)
print("  2010: Senado")
df_sen_2010 = dfs[2010][dfs[2010]['DS_CARGO'].str.contains('SENADOR', na=False)].copy()
if len(df_sen_2010) > 0:
    for (mun, secao), group in df_sen_2010.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in political_data:
            political_data[(mun, secao)] = {}
        political_data[(mun, secao)]['2010_senado'] = {
            'gleisi': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in political_data.keys()]):,} seções")

# 2014: Governador (Gleisi concorreu)
print("  2014: Governador")
df_gov_2014 = dfs[2014][dfs[2014]['DS_CARGO'].str.contains('GOVERNADOR', na=False)].copy()
if len(df_gov_2014) > 0:
    for (mun, secao), group in df_gov_2014.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in political_data:
            political_data[(mun, secao)] = {}
        political_data[(mun, secao)]['2014_governador'] = {
            'gleisi': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in political_data.keys()]):,} seções")

# 2018: Deputada Federal
print("  2018: Deputada Federal")
df_dep_2018 = dfs[2018][dfs[2018]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
if len(df_dep_2018) > 0:
    for (mun, secao), group in df_dep_2018.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in political_data:
            political_data[(mun, secao)] = {}
        political_data[(mun, secao)]['2018_deputado'] = {
            'gleisi': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in political_data.keys()]):,} seções")

# 2022: Deputada Federal
print("  2022: Deputada Federal")
df_dep_2022 = dfs[2022][dfs[2022]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
if len(df_dep_2022) > 0:
    for (mun, secao), group in df_dep_2022.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if (mun, secao) not in political_data:
            political_data[(mun, secao)] = {}
        political_data[(mun, secao)]['2022_deputado'] = {
            'gleisi': int(gleisi_votos),
            'total': int(total)
        }
    print(f"    ✓ {len([k for k in political_data.keys()]):,} seções")

# ===========================================================================
# AGGREGATE BY MUNICIPALITY
# ===========================================================================

print("\n📊 Agregando por município...")

mun_totals = defaultdict(lambda: {
    '2010_senado': {'gleisi': 0, 'total': 0},
    '2014_governador': {'gleisi': 0, 'total': 0},
    '2018_deputado': {'gleisi': 0, 'total': 0},
    '2022_deputado': {'gleisi': 0, 'total': 0},
})

for (mun, secao), years in political_data.items():
    for cargo_ano, data in years.items():
        mun_totals[mun][cargo_ano]['gleisi'] += data['gleisi']
        mun_totals[mun][cargo_ano]['total'] += data['total']

print(f"  ✓ {len(mun_totals)} municípios com dados")

# ===========================================================================
# CALCULATE STATE AVERAGES
# ===========================================================================

print("\n📈 Calculando médias estaduais...")

state_averages = {}
for cargo_ano in ['2010_senado', '2014_governador', '2018_deputado', '2022_deputado']:
    total_gleisi = sum(mun[cargo_ano]['gleisi'] for mun in mun_totals.values())
    total_votos = sum(mun[cargo_ano]['total'] for mun in mun_totals.values())

    pct = (total_gleisi / total_votos * 100) if total_votos > 0 else 0
    state_averages[cargo_ano] = pct

    print(f"  {cargo_ano}: {pct:.2f}%")

# ===========================================================================
# BUILD MUNICIPAL ANALYSIS
# ===========================================================================

print("\n🏛️  Analisando municípios...")

municipal_data = {}

for mun, years in sorted(mun_totals.items()):
    mun_analysis = {
        'municipio': mun,
        'anos': {}
    }

    # Calculate percentages and indices for each year
    for cargo_ano in ['2010_senado', '2014_governador', '2018_deputado', '2022_deputado']:
        year_data = years[cargo_ano]

        gleisi_pct = (year_data['gleisi'] / year_data['total'] * 100) if year_data['total'] > 0 else 0
        gleisi_index = gleisi_pct - state_averages[cargo_ano]

        mun_analysis['anos'][cargo_ano] = {
            'gleisi_pct': round(gleisi_pct, 2),
            'gleisi_index': round(gleisi_index, 3),
            'votos': int(year_data['gleisi']),
            'total_votos': int(year_data['total']),
        }

    # Get 2022 data for classification
    gleisi_2022_pct = mun_analysis['anos']['2022_deputado']['gleisi_pct']
    gleisi_2022_index = mun_analysis['anos']['2022_deputado']['gleisi_index']

    # Trajectory analysis
    pcts = [
        mun_analysis['anos']['2010_senado']['gleisi_pct'],
        mun_analysis['anos']['2014_governador']['gleisi_pct'],
        mun_analysis['anos']['2018_deputado']['gleisi_pct'],
        mun_analysis['anos']['2022_deputado']['gleisi_pct'],
    ]

    if pcts[3] > pcts[0]:
        trajetoria = 'Crescente'
    elif pcts[3] < pcts[0]:
        trajetoria = 'Decrescente'
    else:
        trajetoria = 'Estável'

    mun_analysis['trajetoria'] = trajetoria

    # Gleisi classification (based on 2022)
    if gleisi_2022_index > 3:
        gleisi_class = 'Seguro Gleisi'
    elif gleisi_2022_index > -3:
        gleisi_class = 'Swing'
    else:
        gleisi_class = 'Difícil Gleisi'

    mun_analysis['gleisi_classification'] = gleisi_class

    # Performance index
    avg_index = (mun_analysis['anos']['2010_senado']['gleisi_index'] +
                 mun_analysis['anos']['2014_governador']['gleisi_index'] +
                 mun_analysis['anos']['2018_deputado']['gleisi_index'] +
                 mun_analysis['anos']['2022_deputado']['gleisi_index']) / 4

    mun_analysis['performance_medio'] = round(avg_index, 3)

    municipal_data[mun] = mun_analysis

print(f"  ✓ {len(municipal_data)} municípios analisados")

# ===========================================================================
# STATISTICS
# ===========================================================================

print("\n📊 Estatísticas...")

gleisi_counts = defaultdict(int)
trajetoria_counts = defaultdict(int)

for mun, data in municipal_data.items():
    gleisi_counts[data['gleisi_classification']] += 1
    trajetoria_counts[data['trajetoria']] += 1

print("\n👩‍💼 Classificação Gleisi (2022):")
for classification, count in sorted(gleisi_counts.items()):
    pct = (count / len(municipal_data) * 100)
    print(f"  {classification}: {count} municípios ({pct:.1f}%)")

print("\n📈 Trajetória (2010-2022):")
for trajetoria, count in sorted(trajetoria_counts.items()):
    pct = (count / len(municipal_data) * 100)
    print(f"  {trajetoria}: {count} municípios ({pct:.1f}%)")

# ===========================================================================
# GENERATE DASHBOARD DATA
# ===========================================================================

print("\n📈 Gerando estrutura de dados...")

dashboard_data = {
    'metadata': {
        'projeto': 'Dashboard Eleitoral Paraná 2026',
        'analise': 'Gleisi Hoffmann',
        'anos': [2010, 2014, 2018, 2022],
        'municipios_total': len(municipal_data),
        'data_geracao': '2026-05-30',
        'versao': '2.0-gleisi',
    },
    'estado': {
        'media_estadual': {
            '2010_senado': round(state_averages['2010_senado'], 2),
            '2014_governador': round(state_averages['2014_governador'], 2),
            '2018_deputado': round(state_averages['2018_deputado'], 2),
            '2022_deputado': round(state_averages['2022_deputado'], 2),
        },
        'municipios_count': len(municipal_data),
        'gleisi_distribution': dict(gleisi_counts),
        'trajetoria_distribution': dict(trajetoria_counts),
    },
    'municipios': municipal_data,
}

# ===========================================================================
# SAVE DATA
# ===========================================================================

print("\n💾 Salvando arquivos...")

# Save as JavaScript
with open(OUTPUT_DIR / 'data.js', 'w', encoding='utf-8') as f:
    f.write('const DASHBOARD_DATA = ')
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    f.write(';\n')

print(f"  ✓ data.js ({len(str(dashboard_data)):,} bytes)")

# Save as JSON
with open(OUTPUT_DIR / 'data' / 'dashboard_2026.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"  ✓ data/dashboard_2026.json")

# ===========================================================================
# SUMMARY
# ===========================================================================

print("\n" + "=" * 80)
print("✅ DASHBOARD DATA GENERATION CONCLUÍDO!")
print("=" * 80)

print("\n📊 RESUMO ESTADUAL (Gleisi):")
print(f"  2010 (Senadora): {state_averages['2010_senado']:.2f}%")
print(f"  2014 (Governadora): {state_averages['2014_governador']:.2f}%")
print(f"  2018 (Deputada Federal): {state_averages['2018_deputado']:.2f}%")
print(f"  2022 (Deputada Federal): {state_averages['2022_deputado']:.2f}%")

print("\n✨ O dashboard está pronto para ser testado localmente!")
