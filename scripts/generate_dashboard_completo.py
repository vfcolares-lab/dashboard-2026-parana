#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Paraná 2026 - COMPLETO
Análise bidimensional: Presidencial (PT vs Bolsonaro) + Gleisi Hoffmann
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

BASE_PATH_PR = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/raw')
BASE_PATH_BR = Path('/Users/vitorcolares/Downloads')
OUTPUT_DIR = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana')

print("=" * 80)
print("GERANDO DASHBOARD COMPLETO PARANÁ 2026")
print("Análise: Presidencial (PT vs Bolsonaro) + Gleisi Hoffmann")
print("=" * 80)

# ===========================================================================
# LOAD DATA - PARANÁ (Gleisi)
# ===========================================================================

print("\n📥 Carregando dados do Paraná (Gleisi)...")

dfs_pr = {}
for year in [2010, 2014, 2018, 2022]:
    try:
        df = pd.read_csv(
            BASE_PATH_PR / f'votacao_secao_{year}_PR.csv',
            delimiter=';',
            encoding='latin-1',
            low_memory=False
        )
        df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip().str.upper()
        df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
        df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()
        dfs_pr[year] = df
        print(f"  ✓ {year}: {len(df):,} registros")
    except Exception as e:
        print(f"  ✗ {year}: {e}")
        dfs_pr[year] = pd.DataFrame()

# ===========================================================================
# LOAD DATA - BRASIL (Presidencial)
# ===========================================================================

print("\n📥 Carregando dados presidenciais nacionais (Paraná)...")

dfs_br = {}
for year in [2010, 2014]:
    try:
        filepath = BASE_PATH_BR / f'votacao_secao_{year}_BR' / f'votacao_secao_{year}_BR.csv'
        if not filepath.exists():
            print(f"  ✗ {year}: Arquivo não encontrado em {filepath}")
            dfs_br[year] = pd.DataFrame()
            continue

        # Read full file and filter for PR
        df = pd.read_csv(
            filepath,
            delimiter=';',
            encoding='latin-1',
            low_memory=False
        )
        df = df[df['SG_UF'] == 'PR'].copy()
        df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip().str.upper()
        df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
        df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()
        dfs_br[year] = df
        print(f"  ✓ {year}: {len(df):,} registros (PR apenas)")
    except Exception as e:
        print(f"  ✗ {year}: {e}")
        dfs_br[year] = pd.DataFrame()

# Para 2018 e 2022, vamos usar os dados do Paraná se tiverem presidential
print("  ℹ️  2018 e 2022: Procurando em dados do Paraná...")
for year in [2018, 2022]:
    if year in dfs_pr and len(dfs_pr[year]) > 0:
        df_pres = dfs_pr[year][dfs_pr[year]['DS_CARGO'].str.contains('PRESIDENTE', na=False)]
        if len(df_pres) > 0:
            dfs_br[year] = dfs_pr[year]
            print(f"  ✓ {year}: {len(df_pres):,} registros presidenciais")
        else:
            print(f"  ⚠️  {year}: Dados presidenciais não encontrados")
            dfs_br[year] = pd.DataFrame()

# ===========================================================================
# EXTRACT PRESIDENTIAL DATA
# ===========================================================================

print("\n🗳️  Extraindo dados presidenciais...")

presidential_data = {}

# 2010: Dilma (PT) vs Serra
print("  2010: Presidente (Dilma vs Serra)")
if 2010 in dfs_br and len(dfs_br[2010]) > 0:
    df_pres = dfs_br[2010][dfs_br[2010]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    if len(df_pres) > 0:
        for (mun, secao), group in df_pres.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            dilma = group[group['NM_VOTAVEL'].str.contains('DILMA', case=False, na=False)]['QT_VOTOS'].sum()
            serra = group[group['NM_VOTAVEL'].str.contains('SERRA', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if (mun, secao) not in presidential_data:
                presidential_data[(mun, secao)] = {}
            presidential_data[(mun, secao)]['2010'] = {
                'pt': int(dilma),
                'oposicao': int(serra),
                'total': int(total)
            }
        print(f"    ✓ {len(presidential_data):,} seções")

# 2014: Dilma vs Aécio
print("  2014: Presidente (Dilma vs Aécio)")
if 2014 in dfs_br and len(dfs_br[2014]) > 0:
    df_pres = dfs_br[2014][dfs_br[2014]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    if len(df_pres) > 0:
        for (mun, secao), group in df_pres.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
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

# 2018: Haddad (PT) vs Bolsonaro
print("  2018: Presidente (Haddad vs Bolsonaro)")
if 2018 in dfs_br and len(dfs_br[2018]) > 0:
    df_pres = dfs_br[2018][dfs_br[2018]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    if len(df_pres) > 0:
        for (mun, secao), group in df_pres.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            haddad = group[group['NM_VOTAVEL'].str.contains('HADDAD', case=False, na=False)]['QT_VOTOS'].sum()
            bolsonaro = group[group['NM_VOTAVEL'].str.contains('BOLSONARO', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if (mun, secao) not in presidential_data:
                presidential_data[(mun, secao)] = {}
            presidential_data[(mun, secao)]['2018'] = {
                'pt': int(haddad),
                'oposicao': int(bolsonaro),
                'total': int(total)
            }
        print(f"    ✓ {len([k for k in presidential_data.keys()]):,} seções")

# 2022: Lula vs Bolsonaro
print("  2022: Presidente (Lula vs Bolsonaro)")
if 2022 in dfs_br and len(dfs_br[2022]) > 0:
    df_pres = dfs_br[2022][dfs_br[2022]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    if len(df_pres) > 0:
        for (mun, secao), group in df_pres.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            lula = group[group['NM_VOTAVEL'].str.contains('LULA', case=False, na=False)]['QT_VOTOS'].sum()
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
if 2010 in dfs_pr and len(dfs_pr[2010]) > 0:
    df_sen = dfs_pr[2010][dfs_pr[2010]['DS_CARGO'].str.contains('SENADOR', na=False)].copy()
    if len(df_sen) > 0:
        for (mun, secao), group in df_sen.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if (mun, secao) not in gleisi_data:
                gleisi_data[(mun, secao)] = {}
            gleisi_data[(mun, secao)]['2010'] = {
                'votos': int(gleisi_votos),
                'total': int(total)
            }
        print(f"  ✓ 2010 Senadora: {len([k for k in gleisi_data.keys()]):,} seções")

# 2014: Governadora
if 2014 in dfs_pr and len(dfs_pr[2014]) > 0:
    df_gov = dfs_pr[2014][dfs_pr[2014]['DS_CARGO'].str.contains('GOVERNADOR', na=False)].copy()
    if len(df_gov) > 0:
        for (mun, secao), group in df_gov.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if (mun, secao) not in gleisi_data:
                gleisi_data[(mun, secao)] = {}
            gleisi_data[(mun, secao)]['2014'] = {
                'votos': int(gleisi_votos),
                'total': int(total)
            }
        print(f"  ✓ 2014 Governadora: {len([k for k in gleisi_data.keys()]):,} seções")

# 2018: Deputada Federal
if 2018 in dfs_pr and len(dfs_pr[2018]) > 0:
    df_dep = dfs_pr[2018][dfs_pr[2018]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
    if len(df_dep) > 0:
        for (mun, secao), group in df_dep.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if (mun, secao) not in gleisi_data:
                gleisi_data[(mun, secao)] = {}
            gleisi_data[(mun, secao)]['2018'] = {
                'votos': int(gleisi_votos),
                'total': int(total)
            }
        print(f"  ✓ 2018 Deputada: {len([k for k in gleisi_data.keys()]):,} seções")

# 2022: Deputada Federal
if 2022 in dfs_pr and len(dfs_pr[2022]) > 0:
    df_dep = dfs_pr[2022][dfs_pr[2022]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
    if len(df_dep) > 0:
        for (mun, secao), group in df_dep.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

            if (mun, secao) not in gleisi_data:
                gleisi_data[(mun, secao)] = {}
            gleisi_data[(mun, secao)]['2022'] = {
                'votos': int(gleisi_votos),
                'total': int(total)
            }
        print(f"  ✓ 2022 Deputada: {len([k for k in gleisi_data.keys()]):,} seções")

# ===========================================================================
# AGGREGATE BY MUNICIPALITY
# ===========================================================================

print("\n📊 Agregando dados por município...")

mun_totals = defaultdict(lambda: {
    '2010': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
    '2014': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
    '2018': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
    '2022': {'pt': 0, 'oposicao': 0, 'total': 0, 'gleisi': 0, 'gleisi_total': 0},
})

# Aggregate presidential
for (mun, secao), years in presidential_data.items():
    for year, data in years.items():
        mun_totals[mun][year]['pt'] += data['pt']
        mun_totals[mun][year]['oposicao'] += data['oposicao']
        mun_totals[mun][year]['total'] += data['total']

# Aggregate Gleisi
for (mun, secao), years in gleisi_data.items():
    for year, data in years.items():
        mun_totals[mun][year]['gleisi'] += data['votos']
        mun_totals[mun][year]['gleisi_total'] += data['total']

print(f"  ✓ {len(mun_totals)} municípios com dados agregados")

# ===========================================================================
# CALCULATE STATE AVERAGES
# ===========================================================================

print("\n📈 Calculando médias estaduais...")

state_averages = {}
for year in ['2010', '2014', '2018', '2022']:
    total_pt = sum(mun[year]['pt'] for mun in mun_totals.values())
    total_oposicao = sum(mun[year]['oposicao'] for mun in mun_totals.values())
    total_votos = sum(mun[year]['total'] for mun in mun_totals.values())

    total_gleisi = sum(mun[year]['gleisi'] for mun in mun_totals.values())
    total_gleisi_votos = sum(mun[year]['gleisi_total'] for mun in mun_totals.values())

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

print("\n🏛️  Classificando municípios (análise bidimensional)...")

municipal_data = {}

for mun, years in sorted(mun_totals.items()):
    mun_analysis = {
        'municipio': mun,
        'anos': {}
    }

    # Calculate metrics for each year
    for year in ['2010', '2014', '2018', '2022']:
        year_data = years[year]

        pt_pct = (year_data['pt'] / year_data['total'] * 100) if year_data['total'] > 0 else 0
        oposicao_pct = (year_data['oposicao'] / year_data['total'] * 100) if year_data['total'] > 0 else 0
        gleisi_pct = (year_data['gleisi'] / year_data['gleisi_total'] * 100) if year_data['gleisi_total'] > 0 else 0

        # Federal indices
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

    # Federal classification (2022)
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

    # Gleisi classification (2022)
    gleisi_index_2022 = mun_analysis['anos']['2022']['gleisi_index']

    if gleisi_index_2022 > 3:
        gleisi_class = 'Seguro Gleisi'
    elif gleisi_index_2022 > -3:
        gleisi_class = 'Swing'
    else:
        gleisi_class = 'Difícil Gleisi'

    mun_analysis['gleisi_classification'] = gleisi_class

    municipal_data[mun] = mun_analysis

print(f"  ✓ {len(municipal_data)} municípios classificados")

# ===========================================================================
# STATISTICS
# ===========================================================================

print("\n📊 Estatísticas finais...")

federal_counts = defaultdict(int)
gleisi_counts = defaultdict(int)

for mun, data in municipal_data.items():
    federal_counts[data['federal_classification']] += 1
    gleisi_counts[data['gleisi_classification']] += 1

# ===========================================================================
# GENERATE DASHBOARD DATA
# ===========================================================================

print("\n📈 Gerando estrutura de dados...")

dashboard_data = {
    'metadata': {
        'projeto': 'Dashboard Eleitoral Paraná 2026',
        'analise': 'Bidimensional: Presidencial (PT vs Bolsonaro) + Gleisi Hoffmann',
        'anos': [2010, 2014, 2018, 2022],
        'municipios_total': len(municipal_data),
        'data_geracao': '2026-05-30',
        'versao': '3.0-completo',
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

print(f"  ✓ data.js ({len(str(dashboard_data)):,} bytes)")

# Save as JSON
with open(OUTPUT_DIR / 'data' / 'dashboard_2026_completo.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"  ✓ data/dashboard_2026_completo.json")

# ===========================================================================
# SUMMARY
# ===========================================================================

print("\n" + "=" * 80)
print("✅ DASHBOARD DATA GENERATION COMPLETO!")
print("=" * 80)

print("\n📊 RESUMO ESTADUAL (2022):")
print(f"  PT: {state_averages['2022']['pt_pct']:.2f}%")
print(f"  Bolsonaro: {state_averages['2022']['oposicao_pct']:.2f}%")
print(f"  Gleisi: {state_averages['2022']['gleisi_pct']:.2f}%")

print("\n🏛️  CLASSIFICAÇÃO FEDERAL (Presidencial):")
for classification, count in sorted(federal_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(municipal_data) * 100)
    print(f"  {classification}: {count} municípios ({pct:.1f}%)")

print("\n👩‍💼 CLASSIFICAÇÃO GLEISI:")
for classification, count in sorted(gleisi_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(municipal_data) * 100)
    print(f"  {classification}: {count} municípios ({pct:.1f}%)")

print("\n✨ Dashboard com ANÁLISE BIDIMENSIONAL pronto!")
