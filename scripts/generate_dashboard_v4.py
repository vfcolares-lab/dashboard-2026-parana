#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Paraná 2026 - Versão 4
Classificação por MARGEM (PT - Bolsonaro)
Análise histórica de 2010-2022
Gleisi separada (sem misturar com presidencial)
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

BASE_PATH_BR = Path('/Users/vitorcolares/Downloads')
BASE_PATH_PR = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/raw')
OUTPUT_DIR = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana')

print("=" * 80)
print("DASHBOARD PARANÁ 2026 - V4: CLASSIFICAÇÃO POR MARGEM")
print("Análise: Presidencial (PT vs Bolsonaro) | Gleisi Hoffmann")
print("=" * 80)

# ===========================================================================
# LOAD DATA
# ===========================================================================

print("\n📥 Carregando dados...")

dfs_br = {}
for year in [2010, 2014, 2018, 2022]:
    try:
        filepath = BASE_PATH_BR / f'votacao_secao_{year}_BR' / f'votacao_secao_{year}_BR.csv'
        df = pd.read_csv(filepath, delimiter=';', encoding='latin-1', low_memory=False)
        df = df[df['SG_UF'] == 'PR'].copy()
        df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].str.strip().str.upper()
        df['NM_VOTAVEL'] = df['NM_VOTAVEL'].str.strip()
        df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()
        dfs_br[year] = df
        print(f"  ✓ Presidencial {year}: {len(df):,} registros")
    except Exception as e:
        print(f"  ✗ {year}: {e}")
        dfs_br[year] = pd.DataFrame()

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
        print(f"  ✓ Gleisi {year}: {len(df):,} registros")
    except Exception as e:
        print(f"  ✗ {year}: {e}")
        dfs_pr[year] = pd.DataFrame()

# ===========================================================================
# EXTRACT PRESIDENTIAL DATA BY MUNICIPALITY
# ===========================================================================

print("\n🗳️  Extrai dados presidenciais por município...")

presidential_data = {}

# 2010: Dilma vs Serra
print("  2010: Dilma vs Serra")
if 2010 in dfs_br and len(dfs_br[2010]) > 0:
    df = dfs_br[2010][dfs_br[2010]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    for mun, group in df.groupby('NM_MUNICIPIO'):
        dilma = group[group['NM_VOTAVEL'].str.contains('DILMA', case=False, na=False)]['QT_VOTOS'].sum()
        serra = group[group['NM_VOTAVEL'].str.contains('SERRA', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if mun not in presidential_data:
            presidential_data[mun] = {}

        dilma_pct = (dilma / total * 100) if total > 0 else 0
        serra_pct = (serra / total * 100) if total > 0 else 0
        margem = dilma_pct - serra_pct

        presidential_data[mun]['2010'] = {
            'pt_pct': dilma_pct,
            'oposicao_pct': serra_pct,
            'margem': margem,  # PT - Oposição
            'vencedor': 'PT' if margem > 0 else 'OPOSIÇÃO'
        }
    print(f"    ✓ {len(presidential_data)} municípios")

# 2014: Dilma vs Aécio
print("  2014: Dilma vs Aécio")
if 2014 in dfs_br and len(dfs_br[2014]) > 0:
    df = dfs_br[2014][dfs_br[2014]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    for mun, group in df.groupby('NM_MUNICIPIO'):
        dilma = group[group['NM_VOTAVEL'].str.contains('DILMA', case=False, na=False)]['QT_VOTOS'].sum()
        aecio = group[group['NM_VOTAVEL'].str.contains('AÉCIO|AECIO', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if mun not in presidential_data:
            presidential_data[mun] = {}

        dilma_pct = (dilma / total * 100) if total > 0 else 0
        aecio_pct = (aecio / total * 100) if total > 0 else 0
        margem = dilma_pct - aecio_pct

        presidential_data[mun]['2014'] = {
            'pt_pct': dilma_pct,
            'oposicao_pct': aecio_pct,
            'margem': margem,
            'vencedor': 'PT' if margem > 0 else 'OPOSIÇÃO'
        }
    print(f"    ✓ {len(presidential_data)} municípios")

# 2018: Haddad vs Bolsonaro
print("  2018: Haddad vs Bolsonaro")
if 2018 in dfs_br and len(dfs_br[2018]) > 0:
    df = dfs_br[2018][dfs_br[2018]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    for mun, group in df.groupby('NM_MUNICIPIO'):
        haddad = group[group['NM_VOTAVEL'].str.contains('HADDAD', case=False, na=False)]['QT_VOTOS'].sum()
        bolsonaro = group[group['NM_VOTAVEL'].str.contains('BOLSONARO', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if mun not in presidential_data:
            presidential_data[mun] = {}

        haddad_pct = (haddad / total * 100) if total > 0 else 0
        bolsonaro_pct = (bolsonaro / total * 100) if total > 0 else 0
        margem = haddad_pct - bolsonaro_pct

        presidential_data[mun]['2018'] = {
            'pt_pct': haddad_pct,
            'oposicao_pct': bolsonaro_pct,
            'margem': margem,
            'vencedor': 'PT' if margem > 0 else 'OPOSIÇÃO'
        }
    print(f"    ✓ {len(presidential_data)} municípios")

# 2022: Lula vs Bolsonaro
print("  2022: Lula vs Bolsonaro")
if 2022 in dfs_br and len(dfs_br[2022]) > 0:
    df = dfs_br[2022][dfs_br[2022]['DS_CARGO'].str.contains('PRESIDENTE', na=False)].copy()
    for mun, group in df.groupby('NM_MUNICIPIO'):
        lula = group[group['NM_VOTAVEL'].str.contains('LULA', case=False, na=False)]['QT_VOTOS'].sum()
        bolsonaro = group[group['NM_VOTAVEL'].str.contains('BOLSONARO', case=False, na=False)]['QT_VOTOS'].sum()
        total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()

        if mun not in presidential_data:
            presidential_data[mun] = {}

        lula_pct = (lula / total * 100) if total > 0 else 0
        bolsonaro_pct = (bolsonaro / total * 100) if total > 0 else 0
        margem = lula_pct - bolsonaro_pct

        presidential_data[mun]['2022'] = {
            'pt_pct': lula_pct,
            'oposicao_pct': bolsonaro_pct,
            'margem': margem,
            'vencedor': 'PT' if margem > 0 else 'OPOSIÇÃO'
        }
    print(f"    ✓ {len(presidential_data)} municípios")

# ===========================================================================
# EXTRACT GLEISI DATA
# ===========================================================================

print("\n👩‍💼 Extraindo dados de Gleisi por município...")

gleisi_data = {}

# 2010: Senadora
if 2010 in dfs_pr and len(dfs_pr[2010]) > 0:
    df = dfs_pr[2010][dfs_pr[2010]['DS_CARGO'].str.contains('SENADOR', na=False)].copy()
    if len(df) > 0:
        for mun, group in df.groupby('NM_MUNICIPIO'):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
            if mun not in gleisi_data:
                gleisi_data[mun] = {}
            gleisi_data[mun]['2010'] = (gleisi_votos / total * 100) if total > 0 else 0
        print(f"  ✓ 2010 Senadora: {len(gleisi_data)} municípios")

# 2014: Governadora
if 2014 in dfs_pr and len(dfs_pr[2014]) > 0:
    df = dfs_pr[2014][dfs_pr[2014]['DS_CARGO'].str.contains('GOVERNADOR', na=False)].copy()
    if len(df) > 0:
        for mun, group in df.groupby('NM_MUNICIPIO'):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
            if mun not in gleisi_data:
                gleisi_data[mun] = {}
            gleisi_data[mun]['2014'] = (gleisi_votos / total * 100) if total > 0 else 0
        print(f"  ✓ 2014 Governadora: {len(gleisi_data)} municípios")

# 2018: Deputada
if 2018 in dfs_pr and len(dfs_pr[2018]) > 0:
    df = dfs_pr[2018][dfs_pr[2018]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
    if len(df) > 0:
        for mun, group in df.groupby('NM_MUNICIPIO'):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
            if mun not in gleisi_data:
                gleisi_data[mun] = {}
            gleisi_data[mun]['2018'] = (gleisi_votos / total * 100) if total > 0 else 0
        print(f"  ✓ 2018 Deputada: {len(gleisi_data)} municípios")

# 2022: Deputada
if 2022 in dfs_pr and len(dfs_pr[2022]) > 0:
    df = dfs_pr[2022][dfs_pr[2022]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()
    if len(df) > 0:
        for mun, group in df.groupby('NM_MUNICIPIO'):
            gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
            total = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
            if mun not in gleisi_data:
                gleisi_data[mun] = {}
            gleisi_data[mun]['2022'] = (gleisi_votos / total * 100) if total > 0 else 0
        print(f"  ✓ 2022 Deputada: {len(gleisi_data)} municípios")

# ===========================================================================
# BUILD MUNICIPAL ANALYSIS
# ===========================================================================

print("\n🏛️  Analisando municípios...")

municipal_data = {}

for mun in sorted(presidential_data.keys()):
    pres_data = presidential_data[mun]
    gleisi_pcts = gleisi_data.get(mun, {})

    mun_analysis = {
        'municipio': mun,
        'presidencial': {},
        'gleisi': gleisi_pcts,
        'historico_federal': [],
        'classificacao_2022': None,
    }

    # Presidencial data
    for year in ['2010', '2014', '2018', '2022']:
        if year in pres_data:
            mun_analysis['presidencial'][year] = {
                'pt_pct': round(pres_data[year]['pt_pct'], 2),
                'oposicao_pct': round(pres_data[year]['oposicao_pct'], 2),
                'margem': round(pres_data[year]['margem'], 2),  # PT - Oposição
                'vencedor': pres_data[year]['vencedor']
            }

    # Classificação por MARGEM (2022)
    if '2022' in pres_data:
        margem_2022 = pres_data['2022']['margem']

        if margem_2022 > 10:
            classificacao = 'Bastião Petista'
        elif margem_2022 >= 5:
            classificacao = 'Tendência Petista'
        elif margem_2022 > -5:
            classificacao = 'Swing'
        elif margem_2022 >= -10:
            classificacao = 'Tendência Bolsonarista'
        else:
            classificacao = 'Bastião Bolsonarista'

        mun_analysis['classificacao_2022'] = classificacao

    # Histórico: contar quantas vezes foi cada classificação
    for year in ['2010', '2014', '2018', '2022']:
        if year in pres_data:
            margem = pres_data[year]['margem']

            if margem > 10:
                clase = 'Bastião Petista'
            elif margem >= 5:
                clase = 'Tendência Petista'
            elif margem > -5:
                clase = 'Swing'
            elif margem >= -10:
                clase = 'Tendência Bolsonarista'
            else:
                clase = 'Bastião Bolsonarista'

            mun_analysis['historico_federal'].append({
                'ano': year,
                'classificacao': clase,
                'margem': margem
            })

    municipal_data[mun] = mun_analysis

print(f"  ✓ {len(municipal_data)} municípios analisados")

# ===========================================================================
# STATISTICS
# ===========================================================================

print("\n📊 Estatísticas 2022...")

class_counts = defaultdict(int)
for mun, data in municipal_data.items():
    if data['classificacao_2022']:
        class_counts[data['classificacao_2022']] += 1

for clase, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(municipal_data) * 100)
    print(f"  {clase}: {count} ({pct:.1f}%)")

# ===========================================================================
# GENERATE DASHBOARD DATA
# ===========================================================================

print("\n📈 Gerando dados...")

dashboard_data = {
    'metadata': {
        'projeto': 'Dashboard Eleitoral Paraná 2026',
        'analise': 'Presidencial (por MARGEM) | Gleisi Hoffmann',
        'versao': '4.0-margem',
        'data_geracao': '2026-05-30',
    },
    'municipios': municipal_data,
}

# ===========================================================================
# SAVE
# ===========================================================================

print("\n💾 Salvando...")

with open(OUTPUT_DIR / 'data.js', 'w', encoding='utf-8') as f:
    f.write('const DASHBOARD_DATA = ')
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    f.write(';\n')

print(f"  ✓ data.js")

with open(OUTPUT_DIR / 'data' / 'dashboard_v4_margem.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

print(f"  ✓ data/dashboard_v4_margem.json")

print("\n✅ DASHBOARD V4 PRONTO!")
