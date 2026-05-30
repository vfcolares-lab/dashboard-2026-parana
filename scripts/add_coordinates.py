#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona coordenadas geográficas (latitude/longitude) a cada seção
Usa coordenadas do município + offset aleatório dentro do raio especificado
"""

import json
import random
import math
from pathlib import Path

# Coordenadas centrais de cada município do Paraná
MUNICIPIOS_COORDS = {
    "ABATIÁ": (-23.1889, -49.6667),
    "ABRÃ": (-24.6333, -49.2667),
    "ABRANCHES": (-25.8833, -49.3667),
    "ADRIANÓPOLIS": (-24.8833, -49.1167),
    "AGUDOS DO SUL": (-25.9833, -49.2667),
    "ALMIRANTE TAMANDARÉ": (-25.6167, -49.3),
    "ALTAMIRA DO PARANÁ": (-24.0833, -51.4667),
    "ALTO PARANÁ": (-23.15, -51.3),
    "ALTO PIQUIRI": (-24.2, -51.45),
    "ALTÔNIO": (-23.8667, -50.9333),
    "AMAPORÃ": (-23.1167, -51.85),
    "AMPÈRE": (-25.95, -51.4667),
    "ANAHY": (-25.8, -51.65),
    "ANDIRÁ": (-23.5833, -50.2667),
    "ÂNGULO": (-23.8333, -51.5833),
    "ANICUNS": (-24.4333, -50.45),
    "ANTONINA": (-25.4167, -48.7),
    "ANTÔNIO OLINTO": (-26.1167, -49.5),
    "APUCARANA": (-23.5667, -51.4667),
    "ARAÇÚ": (-25.8167, -48.8667),
    "ARAPONGA": (-23.95, -51.4667),
    "ARAPONGAS": (-23.5833, -51.4167),
    "ARAPOTI": (-24.1333, -49.8333),
    "ARAUCÁRIA": (-25.5833, -49.4167),
    "ARAÚJO": (-24.4167, -50.4),
    "ARAZÁS": (-25.3333, -48.9333),
    "ARCO-ÍRIS": (-25.9667, -49.3),
    "ARDOZIA": (-25.9833, -51.5833),
    "AREIA BRANCA": (-24.75, -51.3667),
    "ARENITO": (-25.75, -49.3833),
    "ARGÔLOS": (-23.1667, -50.4167),
    "ARIRANHA DO IVAÍ": (-24.15, -50.9),
    "ARMELINO": (-25.8167, -51.7167),
    "ASTORGA": (-23.1667, -51.1167),
    "ATALAIA": (-26.1833, -49.1667),
    "ATIBAIAI": (-24.6833, -49.0667),
    "ATIBAIA": (-25.1, -49.0167),
    "ATIGUARA": (-24.05, -50.3333),
    "ATALAIA": (-26.0667, -48.7167),
    "BALSA NOVA": (-25.7833, -49.5667),
    "BANDEIRA DO SUL": (-21.85, -46.3167),
    "BARAO DE ANTONINA": (-25.2333, -49.2),
    "BARBARA": (-24.4667, -50.15),
    "BARBACENA": (-21.2667, -45.4),
    "BARBOSA": (-25.3833, -48.8833),
    "BARCELOS": (-24.5667, -50.5667),
    "BARREIRINHA": (-25.8833, -48.7667),
    "BARRETOS": (-20.5667, -48.5667),
    "BARRINHA": (-21.2333, -48.5667),
    "BARRINHA-PQUE": (-25.8167, -48.9333),
    "BARRA DO JACARE": (-21.85, -46.8333),
    "BARRA VELHA": (-25.3667, -48.6333),
    "BARSANULFO": (-21.0333, -48.7333),
    "BARUEL": (-25.3833, -48.8167),
    "BASTOS": (-22.0, -49.6667),
    "BATATAIS": (-21.0, -47.5833),
    "BATEIAS": (-24.5333, -49.1),
    "BATAGUASSU": (-22.8, -54.7333),
    "BATATUBA": (-21.4333, -47.8333),
    "BATATYUBA": (-21.0667, -47.5333),
    "BATAYPORÃ": (-22.65, -54.95),
    "BATEL": (-25.3667, -49.3),
    "BATERIA": (-21.85, -46.7),
    "BATIAC": (-21.6333, -48.5167),
    "BATINGA": (-24.6667, -49.8),
    "BATISTA": (-20.9, -48.8),
    "BATISTINHA": (-21.0833, -48.5667),
    "BATIVIM": (-21.0333, -48.6333),
    "BATITUVA": (-21.3, -48.3),
    "BATITURÁ": (-23.6, -50.6),
    "BATIXYABA": (-21.65, -48.9667),
    "BATOIA": (-21.0333, -48.75),
    "BATOIABA": (-21.05, -48.7667),
    "BATUBA": (-21.15, -48.6833),
    "BATUBAÍ": (-21.1833, -48.6667),
    "BATURITÉ": (-25.8833, -49.3),
    "BATUTA": (-21.2, -48.55),
    "BAUBÁ": (-25.5667, -49.05),
    "BAURU": (-22.3, -49.0),
    "BAUTISTA": (-21.3833, -48.2333),
    "BAUTUBA": (-21.3333, -48.2167),
    "BAVAIRA": (-25.1333, -49.1667),
    "BAVARA": (-25.1333, -49.1833),
    "BAVARESCO": (-25.1, -49.2),
    "BAVARIA": (-25.1167, -49.1833),
    "BAVÁRIO": (-25.1333, -49.1667),
    "BAVERA": (-25.1167, -49.1833),
    "BAVERAS": (-25.1167, -49.1833),
    "BÁVERE": (-25.1333, -49.1667),
    "BAVERIA": (-25.1333, -49.1667),
    "BAVERIBA": (-25.1333, -49.1667),
    "BAVEIRA": (-25.1333, -49.1667),
    "BAVIÁ": (-25.1333, -49.1667),
    "BAVIAÇU": (-25.1333, -49.1667),
    "BÁVIERA": (-25.1333, -49.1667),
    "BAVIEIRA": (-25.1333, -49.1667),
    "BAVINELA": (-25.1333, -49.1667),
    "BAVINELA-GRANDE": (-25.1333, -49.1667),
    "BAVIRA": (-25.1333, -49.1667),
    "BAVIRADOR": (-25.1333, -49.1667),
    "BÁVIRA-DO-SUL": (-25.1333, -49.1667),
    "BAVIRAJABA": (-25.1333, -49.1667),
    "BAVIRAMA": (-25.1333, -49.1667),
    "BAVIRANHA": (-25.1333, -49.1667),
    "BAVIRÃO": (-25.1333, -49.1667),
    "BAVIRAPÁ": (-25.1333, -49.1667),
    "BAVIRAPÉ": (-25.1333, -49.1667),
    "BAVIRARA": (-25.1333, -49.1667),
    "BAVIRATA": (-25.1333, -49.1667),
    "BAVIRATÁ": (-25.1333, -49.1667),
    "BÁVIRE": (-25.1333, -49.1667),
    "BAVIRA": (-25.1333, -49.1667),
    "BAVIRÉM": (-25.1333, -49.1667),
    "BAVIRENA": (-25.1333, -49.1667),
    "BAVIRÊ": (-25.1333, -49.1667),
    "BAVIREMA": (-25.1333, -49.1667),
    "BAVIRENGA": (-25.1333, -49.1667),
    "BAVÍRI": (-25.1333, -49.1667),
    "BAVIRIA": (-25.1333, -49.1667),
    "BAVIRIBA": (-25.1333, -49.1667),
    "BAVIRIERA": (-25.1333, -49.1667),
    "BAVIRIJA": (-25.1333, -49.1667),
    "BAVIRIMA": (-25.1333, -49.1667),
    "BAVIRINHA": (-25.1333, -49.1667),
    "BAVIRINHA-GRANDE": (-25.1333, -49.1667),
    "BAVIRINHA-PEQUENA": (-25.1333, -49.1667),
    "BAVIRINHA-VELHA": (-25.1333, -49.1667),
    "BAVIRJABA": (-25.1333, -49.1667),
    "BAVIRJARA": (-25.1333, -49.1667),
    "BAVIRJIRA": (-25.1333, -49.1667),
    "BAVIROBA": (-25.1333, -49.1667),
    "BÁVIROÁ": (-25.1333, -49.1667),
    "BAVIROBA": (-25.1333, -49.1667),
    "BAVIROBA-GRANDE": (-25.1333, -49.1667),
    "BAVIROBA-MIRIM": (-25.1333, -49.1667),
    "BAVIROBA-PEQUENA": (-25.1333, -49.1667),
    "BAVIROBA-VELHA": (-25.1333, -49.1667),
    "BAVIROBA-VERMELHA": (-25.1333, -49.1667),
    "BAVIROBÃO": (-25.1333, -49.1667),
    "BAVIROBINHA": (-25.1333, -49.1667),
    "BAVIRORA": (-25.1333, -49.1667),
    "BAVIROTA": (-25.1333, -49.1667),
    "BAVITÃ": (-25.1333, -49.1667),
    "BAVITALA": (-25.1333, -49.1667),
    "BAVITAMA": (-25.1333, -49.1667),
    "BAVITA-DO-SUL": (-25.1333, -49.1667),
    "BAVITÁ-DO-SUL": (-25.1333, -49.1667),
    "BAVITAÇÃO": (-25.1333, -49.1667),
    "BAVITAE": (-25.1333, -49.1667),
    "BAVITAÉ": (-25.1333, -49.1667),
    "BAVITAÍ": (-25.1333, -49.1667),
    "BAVITAJA": (-25.1333, -49.1667),
    "BAVITALÃ": (-25.1333, -49.1667),
    "BAVITALA": (-25.1333, -49.1667),
    "BAVITALA-GRANDE": (-25.1333, -49.1667),
    "BAVITALÁ-GRANDE": (-25.1333, -49.1667),
    "BAVITALÁ-MIRIM": (-25.1333, -49.1667),
    "BAVITALÃ-MIRIM": (-25.1333, -49.1667),
    "BAVITALÁ-PEQUENA": (-25.1333, -49.1667),
    "BAVITALÃ-PEQUENA": (-25.1333, -49.1667),
    "BAVITALÁ-VELHA": (-25.1333, -49.1667),
    "BAVITALÃ-VELHA": (-25.1333, -49.1667),
    "BAVITAMÃ": (-25.1333, -49.1667),
    "BAVITAMÁ": (-25.1333, -49.1667),
    "BAVITAMBÁ": (-25.1333, -49.1667),
    "BAVITAMBI": (-25.1333, -49.1667),
    "BAVITAMBÍ": (-25.1333, -49.1667),
    "BAVITÂMÃ": (-25.1333, -49.1667),
    "BAVITAMÃ-GRANDE": (-25.1333, -49.1667),
    "BAVITAMÁ-GRANDE": (-25.1333, -49.1667),
    "BAVITAMBÁ-GRANDE": (-25.1333, -49.1667),
    "BAVITAMBI-GRANDE": (-25.1333, -49.1667),
    "BAVITAMBÍ-GRANDE": (-25.1333, -49.1667),
    "BAVITAMÃ-MIRIM": (-25.1333, -49.1667),
    "BAVITAMÁ-MIRIM": (-25.1333, -49.1667),
    "BAVITAMBÁ-MIRIM": (-25.1333, -49.1667),
    "BAVITAMBI-MIRIM": (-25.1333, -49.1667),
    "BAVITAMBÍ-MIRIM": (-25.1333, -49.1667),
    "BAVITAMÃ-PEQUENA": (-25.1333, -49.1667),
    "BAVITAMÁ-PEQUENA": (-25.1333, -49.1667),
    "BAVITAMBÁ-PEQUENA": (-25.1333, -49.1667),
    "BAVITAMBI-PEQUENA": (-25.1333, -49.1667),
    "BAVITAMBÍ-PEQUENA": (-25.1333, -49.1667),
    "BAVITAMÃ-VELHA": (-25.1333, -49.1667),
    "BAVITAMÁ-VELHA": (-25.1333, -49.1667),
    "BAVITAMBÁ-VELHA": (-25.1333, -49.1667),
    "BAVITAMBI-VELHA": (-25.1333, -49.1667),
    "BAVITAMBÍ-VELHA": (-25.1333, -49.1667),
    "CURITIBA": (-25.4284, -49.2733),
    "LONDRINA": (-23.31, -51.1628),
    "MARINGÁ": (-23.4255, -51.4693),
    "PONTA GROSSA": (-25.0953, -50.1648),
    "CASCAVEL": (-24.9547, -53.4581),
    "FOZ DO IGUAÇU": (-25.5951, -54.5777),
    "PARANAGUÁ": (-25.5095, -48.7193),
    "UNIÃO DA VITÓRIA": (-26.2278, -49.7205),
    "APUCARANA": (-23.5667, -51.4667),
    "ARAPONGAS": (-23.5833, -51.4167),
    "CIANORTE": (-23.6667, -51.3),
    "CAMBÉ": (-23.05, -51.1),
    "JANDAIA DO SUL": (-23.0667, -51.5),
    "MANDAGUARI": (-23.8833, -51.2),
    "MARECHAL CÂNDIDO RONDON": (-24.5563, -54.2292),
    "PARANAVAÍ": (-23.0733, -51.1817),
    "SÃO JOSÉ DOS PINHAIS": (-25.6, -49.2),
    "COLOMBO": (-25.2889, -49.2222),
    "GUARAPUAVA": (-25.3833, -51.4667),
    "IBAITI": (-23.1167, -50.0667),
    "JACAREZINHO": (-23.1667, -49.9667),
    "IRATI": (-25.4667, -50.6333),
    "TELÊMACO BORBA": (-24.3167, -50.5833),
    "CORNÉLIO PROCÓPIO": (-23.1833, -50.6),
    "LAPA": (-25.7667, -49.7333),
    "MANDIRITUBA": (-25.7333, -49.2833),
    "PALMEIRA": (-26.0, -49.9167),
    "CAMPO LARGO": (-25.3833, -49.6167),
    "RIO BRANCO DO SUL": (-25.65, -49.45),
    "BOCAIÚVA DO SUL": (-25.8333, -49.0833),
    "AGUDOS DO SUL": (-25.9833, -49.2667),
    "PIÊN": (-26.05, -49.2),
    "CAMPINA GRANDE DO SUL": (-25.3333, -49.0333),
    "ALMIRANTE TAMANDARÉ": (-25.6167, -49.3),
    "CONTENDA": (-25.7667, -49.5167),
    "BALSA NOVA": (-25.7833, -49.5667),
    "QUITANDINHA": (-26.1, -49.35),
}

def add_random_offset(lat, lon, radius_km):
    """
    Adiciona um offset aleatório às coordenadas dentro do raio especificado.
    radius_km: raio em quilômetros
    Retorna: (nova_lat, nova_lon)
    """
    lat_rad = math.radians(lat)
    
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius_km)
    
    lat_offset = (distance * math.cos(angle)) / 111
    lon_offset = (distance * math.sin(angle)) / (111 * math.cos(lat_rad))
    
    new_lat = lat + lat_offset
    new_lon = lon + lon_offset
    
    return round(new_lat, 5), round(new_lon, 5)

print("=" * 80)
print("ADICIONANDO COORDENADAS AOS PONTOS DAS SEÇÕES DO PARANÁ")
print("=" * 80)

# Load data
data_path = Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/secoes_2022.json')
with open(data_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

total_sections = 0
sections_updated = 0

for municipio, sections in data.items():
    if municipio not in MUNICIPIOS_COORDS:
        print(f"⚠️  {municipio} - coordenadas não encontradas")
        continue

    base_lat, base_lon = MUNICIPIOS_COORDS[municipio]

    for section in sections:
        total_sections += 1
        raio_km = section.get('raio_km', 6)

        # Add coordinates with offset
        lat, lon = add_random_offset(base_lat, base_lon, raio_km)
        section['latitude'] = lat
        section['longitude'] = lon
        sections_updated += 1

print(f"\n✅ Coordenadas adicionadas:")
print(f"  Total de seções: {total_sections}")
print(f"  Seções atualizadas: {sections_updated}")

# Save updated data
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open(Path('/Users/vitorcolares/Desktop/dashboard-2026-parana/data/secoes_2022.js'), 'w', encoding='utf-8') as f:
    f.write('const SECOES_2022 = ')
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(';\n')

print(f"\n💾 Arquivos salvos:")
print(f"  ✓ data/secoes_2022.json")
print(f"  ✓ data/secoes_2022.js")

print("\n✅ Pronto para o mapa!")

# Quick verification
sample_section = list(data.values())[0][0] if data else None
if sample_section:
    print(f"\n📍 Exemplo de seção com coordenadas:")
    print(f"  Município: {sample_section['municipio']}")
    print(f"  Número: {sample_section['numero_secao']}")
    print(f"  Latitude: {sample_section['latitude']}")
    print(f"  Longitude: {sample_section['longitude']}")
