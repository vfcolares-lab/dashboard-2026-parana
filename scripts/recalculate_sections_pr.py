#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recalculate voting sections for Paraná 2026 dashboard
Analyzes Gleisi Hoffmann performance across 4 elections (2010-2022)
"""

import pandas as pd
import json
from pathlib import Path
import sys

BASE_PATH = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/raw')

print("=" * 80)
print("RECALCULANDO SEÇÕES ELEITORAIS DO PARANÁ COM GLEISI HOFFMANN")
print("=" * 80)

# ===========================================================================
# LOAD DATA FILES
# ===========================================================================

print("\n📥 Carregando arquivos de dados...")

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
        df['DS_CARGO'] = df['DS_CARGO'].str.strip().str.upper()  # Normalize cargo names
        dfs[year] = df
        print(f"  ✓ {year}: {len(df)} registros")
    except Exception as e:
        print(f"  ✗ {year}: {e}")
        dfs[year] = pd.DataFrame()

# ===========================================================================
# EXTRACT RELEVANT ELECTIONS
# ===========================================================================

print("\n🔄 Separando dados por tipo de cargo...")

# 2010: Senador (majoritário - 2 vagas)
df_sen_2010 = dfs[2010][dfs[2010]['DS_CARGO'].str.contains('SENADOR', na=False)].copy() if len(dfs[2010]) > 0 else pd.DataFrame()

# 2014: Governador (Gleisi foi candidata)
df_gov_2014 = dfs[2014][dfs[2014]['DS_CARGO'].str.contains('GOVERNADOR', na=False)].copy() if len(dfs[2014]) > 0 else pd.DataFrame()

# 2018: Deputado Federal (proporcional)
df_dep_2018 = dfs[2018][dfs[2018]['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy() if len(dfs[2018]) > 0 else pd.DataFrame()

# 2022: Verificar qual cargo Gleisi concorreu
df_2022 = dfs[2022]
gleisi_records_2022 = df_2022[df_2022['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]
if len(gleisi_records_2022) > 0:
    cargo_2022 = gleisi_records_2022['DS_CARGO'].unique()[0]
    print(f"  Gleisi em 2022 concorreu a: {cargo_2022}")
    df_dep_2022 = df_2022[df_2022['DS_CARGO'] == cargo_2022].copy()
else:
    # Default para Deputado Federal se não encontrar
    df_dep_2022 = df_2022[df_2022['DS_CARGO'].str.contains('DEPUTADO FEDERAL', na=False)].copy()

print(f"  2010 Senador: {len(df_sen_2010)}")
print(f"  2014 Governador: {len(df_gov_2014)}")
print(f"  2018 Deputado Federal: {len(df_dep_2018)}")
print(f"  2022: {len(df_dep_2022)} (cargo: {df_dep_2022['DS_CARGO'].unique()[0] if len(df_dep_2022) > 0 else 'N/A'})")

# ===========================================================================
# AGGREGATE BY SECTION - GLEISI
# ===========================================================================

print("\n🔄 Agregando dados de Gleisi por seção...")

sections_data = {}

# 2010 Senatorial (divide by 2 - 2 spots)
sen_2010_agg = {}
if len(df_sen_2010) > 0:
    for (mun, secao), group in df_sen_2010.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total_votos = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        sen_2010_agg[(mun, secao)] = {
            'gleisi': gleisi_votos / 2,  # Divide by 2 for 2 spots
            'total': total_votos
        }
    print(f"  ✓ 2010 senatorial: {len(sen_2010_agg)} seções com dados")

# 2014 Gubernatorial
gov_2014_agg = {}
if len(df_gov_2014) > 0:
    for (mun, secao), group in df_gov_2014.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total_votos = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        gov_2014_agg[(mun, secao)] = {
            'gleisi': gleisi_votos,
            'total': total_votos
        }
    print(f"  ✓ 2014 gubernatorial: {len(gov_2014_agg)} seções com dados")

# 2018 Federal Deputy
dep_2018_agg = {}
if len(df_dep_2018) > 0:
    for (mun, secao), group in df_dep_2018.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total_votos = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        dep_2018_agg[(mun, secao)] = {
            'gleisi': gleisi_votos,
            'total': total_votos
        }
    print(f"  ✓ 2018 federal deputy: {len(dep_2018_agg)} seções com dados")

# 2022
dep_2022_agg = {}
endereco_map = {}
if len(df_dep_2022) > 0:
    for (mun, secao), group in df_dep_2022.groupby(['NM_MUNICIPIO', 'NR_SECAO']):
        gleisi_votos = group[group['NM_VOTAVEL'].str.contains('GLEISI', case=False, na=False)]['QT_VOTOS'].sum()
        total_votos = group[~group['NM_VOTAVEL'].str.contains('NULO|BRANCO', na=False)]['QT_VOTOS'].sum()
        dep_2022_agg[(mun, secao)] = {
            'gleisi': gleisi_votos,
            'total': total_votos
        }
        
        # Get address
        endereco = group['DS_LOCAL_VOTACAO_ENDERECO'].iloc[0] if 'DS_LOCAL_VOTACAO_ENDERECO' in group.columns and pd.notna(group['DS_LOCAL_VOTACAO_ENDERECO'].iloc[0]) else f"SEÇÃO {secao}"
        endereco_map[(mun, secao)] = endereco
    
    print(f"  ✓ 2022: {len(dep_2022_agg)} seções com dados")

# ===========================================================================
# BUILD COMPREHENSIVE SECTION DATA
# ===========================================================================

print("\n🔨 Construindo dados das seções...")

# Use 2022 as base for all sections
for (mun, secao), dados_2022 in dep_2022_agg.items():
    if mun not in sections_data:
        sections_data[mun] = []

    # 2022
    gleisi_2022 = dados_2022['gleisi']
    total_2022 = dados_2022['total']
    gleisi_pct_2022 = (gleisi_2022 / total_2022 * 100) if total_2022 > 0 else 0

    # 2018
    gleisi_2018 = 0
    gleisi_pct_2018 = 0
    if (mun, secao) in dep_2018_agg:
        dados_2018 = dep_2018_agg[(mun, secao)]
        gleisi_2018 = dados_2018['gleisi']
        total_2018 = dados_2018['total']
        gleisi_pct_2018 = (gleisi_2018 / total_2018 * 100) if total_2018 > 0 else 0

    # 2014
    gleisi_2014 = 0
    gleisi_pct_2014 = 0
    if (mun, secao) in gov_2014_agg:
        dados_2014 = gov_2014_agg[(mun, secao)]
        gleisi_2014 = dados_2014['gleisi']
        total_2014 = dados_2014['total']
        gleisi_pct_2014 = (gleisi_2014 / total_2014 * 100) if total_2014 > 0 else 0

    # 2010
    gleisi_2010 = 0
    gleisi_pct_2010 = 0
    if (mun, secao) in sen_2010_agg:
        dados_2010 = sen_2010_agg[(mun, secao)]
        gleisi_2010 = dados_2010['gleisi']
        total_2010 = dados_2010['total']
        gleisi_pct_2010 = (gleisi_2010 / total_2010 * 100) if total_2010 > 0 else 0

    # Volatilidade
    volatilidade = abs(gleisi_pct_2022 - gleisi_pct_2018) / 100 if gleisi_pct_2018 > 0 else 0

    # Trajetória (crescente, decrescente, estável)
    trajetoria = 'N/A'
    if gleisi_pct_2010 > 0 and gleisi_pct_2014 > 0 and gleisi_pct_2018 > 0 and gleisi_pct_2022 > 0:
        if gleisi_pct_2022 > gleisi_pct_2018:
            trajetoria = 'crescente'
        elif gleisi_pct_2022 < gleisi_pct_2018:
            trajetoria = 'decrescente'
        else:
            trajetoria = 'estavel'

    # Address
    endereco = endereco_map.get((mun, secao), f"SEÇÃO {secao}")

    section_obj = {
        'numero_secao': int(secao),
        'municipio': mun,
        'endereco': endereco,
        'votos_gleisi': {
            '2010_senado': int(gleisi_2010),
            '2010_pct': round(gleisi_pct_2010, 1),
            '2014_governador': int(gleisi_2014),
            '2014_pct': round(gleisi_pct_2014, 1),
            '2018_deputado': int(gleisi_2018),
            '2018_pct': round(gleisi_pct_2018, 1),
            '2022_deputado': int(gleisi_2022),
            '2022_pct': round(gleisi_pct_2022, 1),
        },
        'trajetoria': trajetoria,
        'volatilidade': round(volatilidade, 2),
        'latitude': None,
        'longitude': None,
        'raio_km': 6,
    }

    sections_data[mun].append(section_obj)

# ===========================================================================
# STATISTICS
# ===========================================================================

print("\n📈 Estatísticas:")
total_sections = 0
mun_count = 0

for mun, sections in sections_data.items():
    total_sections += len(sections)
    if len(sections) > 0:
        mun_count += 1

print(f"  ✅ Total de seções: {total_sections}")
print(f"  ✅ Municípios com dados: {mun_count}")

# ===========================================================================
# SAVE DATA
# ===========================================================================

print("\n💾 Salvando dados...")

# Save as JSON
with open(Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data') / 'secoes_2022.json', 'w', encoding='utf-8') as f:
    json.dump(sections_data, f, indent=2, ensure_ascii=False)

# Save as JavaScript
with open(Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data') / 'secoes_2022.js', 'w', encoding='utf-8') as f:
    f.write('const SECOES_2022 = ')
    json.dump(sections_data, f, indent=2, ensure_ascii=False)
    f.write(';\n')

print("  ✓ data/secoes_2022.json")
print("  ✓ data/secoes_2022.js")

print("\n✅ Processamento de seções concluído!")
print("\nPróximo passo: executar add_coordinates.py para adicionar latitude/longitude")
