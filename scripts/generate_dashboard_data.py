#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate DASHBOARD_DATA for Paraná dashboard
Aggregates data by municipality from secoes_2022.json
"""

import json
from pathlib import Path
from collections import defaultdict

# Load sections data
with open(Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/secoes_2022.json'), 'r', encoding='utf-8') as f:
    sections_data = json.load(f)

print("=" * 80)
print("GERANDO DASHBOARD_DATA PARA PARANÁ")
print("=" * 80)

# Aggregate by municipality
municipios_data = {}

for municipio, secoes in sections_data.items():
    if not secoes:
        continue
    
    # Aggregate votes
    total_votos_gleisi_2010 = sum(s['votos_gleisi']['2010_senado'] for s in secoes)
    total_votos_gleisi_2014 = sum(s['votos_gleisi']['2014_governador'] for s in secoes)
    total_votos_gleisi_2018 = sum(s['votos_gleisi']['2018_deputado'] for s in secoes)
    total_votos_gleisi_2022 = sum(s['votos_gleisi']['2022_deputado'] for s in secoes)
    
    # Calculate percentages (from first seção)
    pct_2010 = secoes[0]['votos_gleisi']['2010_pct']
    pct_2014 = secoes[0]['votos_gleisi']['2014_pct']
    pct_2018 = secoes[0]['votos_gleisi']['2018_pct']
    pct_2022 = secoes[0]['votos_gleisi']['2022_pct']
    
    municipios_data[municipio] = {
        "gleisi": {
            "2010": {"votos_pct": pct_2010},
            "2014": {"votos_pct": pct_2014},
            "2018": {"votos_pct": pct_2018},
            "2022": {"votos_pct": pct_2022}
        },
        "trajetoria": secoes[0].get('trajetoria', 'N/A'),
        "volatilidade": secoes[0].get('volatilidade', 0),
        "num_secoes": len(secoes)
    }

# Calculate state averages
total_gleisi_2010 = sum(s['votos_gleisi']['2010_senado'] for secoes in sections_data.values() for s in secoes)
total_gleisi_2014 = sum(s['votos_gleisi']['2014_governador'] for secoes in sections_data.values() for s in secoes)
total_gleisi_2018 = sum(s['votos_gleisi']['2018_deputado'] for secoes in sections_data.values() for s in secoes)
total_gleisi_2022 = sum(s['votos_gleisi']['2022_deputado'] for secoes in sections_data.values() for s in secoes)

total_votos_2010 = sum(s['votos_gleisi'].get('2010_votos_totais', 0) for secoes in sections_data.values() for s in secoes) or 1
total_votos_2022 = sum(s['votos_gleisi'].get('2022_votos_totais', 0) for secoes in sections_data.values() for s in secoes) or 1

# Build DASHBOARD_DATA
dashboard_data = {
    "metadata": {
        "generated_at": "2026-05-30T00:00:00",
        "version": "1.0",
        "state": "Paraná",
        "total_municipalities": len(municipios_data),
        "total_sections": sum(len(secoes) for secoes in sections_data.values()),
        "candidate": "Gleisi Hoffmann",
        "elections": [2010, 2014, 2018, 2022]
    },
    "estado": {
        "gleisi": {
            "2010": {
                "votos_pct": round(total_gleisi_2010 / max(total_votos_2010, 1) * 100, 1),
                "total_votos": int(total_gleisi_2010)
            },
            "2014": {
                "votos_pct": round(total_gleisi_2014 / max(total_votos_2022, 1) * 100, 1),
                "total_votos": int(total_gleisi_2014)
            },
            "2018": {
                "votos_pct": round(total_gleisi_2018 / max(total_votos_2022, 1) * 100, 1),
                "total_votos": int(total_gleisi_2018)
            },
            "2022": {
                "votos_pct": round(total_gleisi_2022 / max(total_votos_2022, 1) * 100, 1),
                "total_votos": int(total_gleisi_2022)
            }
        }
    },
    "municipios": municipios_data
}

# Save
output_path = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data.js')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('const DASHBOARD_DATA = ')
    json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    f.write(';\n')

print(f"\n✅ Arquivo gerado: {output_path}")
print(f"   Municípios: {len(municipios_data)}")
print(f"   Total de seções: {sum(len(secoes) for secoes in sections_data.values())}")
print(f"\n💾 Não esqueça de copiar data.js para a raiz do projeto!")
