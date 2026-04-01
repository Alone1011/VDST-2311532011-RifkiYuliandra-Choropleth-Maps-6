import json
import pandas as pd
import numpy as np
import os
import re
import random

def standardize_name(name):
    if not isinstance(name, str): return ""
    name = name.lower()
    name = name.replace("kab.", "").replace("kota", "").strip()
    # Handle known aliases
    if name == "padangpanjang": name = "padang panjang"
    if name == "sawah lunto": name = "sawahlunto"
    return name

def parse_double_encoded_json(coord_str):
    if isinstance(coord_str, str):
        try:
            parsed1 = json.loads(coord_str)
            if isinstance(parsed1, str):
                parsed2 = json.loads(parsed1)
                return parsed2
            return parsed1
        except Exception:
            pass
    return coord_str

# Read JSON
print("Reading adm2.json..")
with open('geojson-id-master/data/adm2.json/adm2.json', 'r', encoding='utf-8') as f:
    adm2_data = json.load(f)

print("Reading adm3.json..")
with open('geojson-id-master/data/adm3.json/adm3.json', 'r', encoding='utf-8') as f:
    adm3_data = json.load(f)

# Filter for Sumatera Barat
sumbar_kab = [d for d in adm2_data if 'SUMATERA BARAT' in str(d.get('adm1', '')).upper()]
sumbar_kec = [d for d in adm3_data if 'SUMATERA BARAT' in str(d.get('adm1', '')).upper()]

# Build standard GeoJSON structures
def build_feature(d):
    geom_data = parse_double_encoded_json(d.get('coordinates'))
    # Extract only geometry if it's a FeatureCollection
    geometry = None
    if isinstance(geom_data, dict) and geom_data.get('type') == 'FeatureCollection':
        if len(geom_data.get('features', [])) > 0:
            raw_geom = geom_data['features'][0].get('geometry')
            if isinstance(raw_geom, str):
                try: geometry = json.loads(raw_geom)
                except: geometry = raw_geom
            else:
                geometry = raw_geom
    elif isinstance(geom_data, dict) and geom_data.get('type') in ['Polygon', 'MultiPolygon']:
        geometry = geom_data
    elif isinstance(geom_data, str):
        try:
            parsed = json.loads(geom_data)
            if parsed.get('type') in ['Polygon', 'MultiPolygon']:
                geometry = parsed
            elif parsed.get('type') == 'Feature':
                raw_geom = parsed.get('geometry')
                if isinstance(raw_geom, str):
                    try: geometry = json.loads(raw_geom)
                    except: geometry = raw_geom
                else:
                    geometry = raw_geom
        except: pass

    # Skip invalid geometries or purely "Danau" properties
    name = d.get('name', '')
    if 'danau' in name.lower():
        return None

    props = {
        'name': name,
        'std_name': standardize_name(name),
        'id': d.get('id'),
        'adm1': d.get('adm1'),
        'adm2': d.get('adm2', name)
    }

    return {
        "type": "Feature",
        "properties": props,
        "geometry": geometry
    }

feature_kab = []
for k in sumbar_kab:
    f = build_feature(k)
    if f and f['geometry']:
        feature_kab.append(f)

feature_kec = []
for k in sumbar_kec:
    f = build_feature(k)
    if f and f['geometry']:
        f['properties']['kecamatan'] = f['properties']['name']
        f['properties']['kabupaten'] = k.get('adm2', '')
        feature_kec.append(f)

print(f"Total valid Kabupaten: {len(feature_kab)}")
print(f"Total valid Kecamatan: {len(feature_kec)}")

# Initialize data dict per Kabupaten
data_by_kab = {}
for f in feature_kab:
    data_by_kab[f['properties']['std_name']] = {}

# Process CSV files
dataset_dir = 'dataset'
csv_files = [f for f in os.listdir(dataset_dir) if f.endswith('.csv')]

def clean_val(val):
    if pd.isna(val) or val == '-': return None
    try:
        return float(str(val).replace(',', '.'))
    except:
        return None

for csv_f in csv_files:
    path = os.path.join(dataset_dir, csv_f)
    print(f"Processing {csv_f}...")
    
    if 'Indeks Pembangunan Manusia' in csv_f:
        df = pd.read_csv(path, header=None)
        # SP2010 starts at col 1 (idx 1: 2015, ..., 5: 2019) -> wait, the header shows years
        years_1 = df.iloc[1, 1:11].tolist() # 2015-2024
        years_2 = df.iloc[1, 11:17].tolist() # 2020-2025
        for i in range(2, len(df)):
            kab = standardize_name(df.iloc[i, 0])
            if kab not in data_by_kab: continue
            # 2015-2019 from table 1
            for j in range(5): 
                val = clean_val(df.iloc[i, j+1])
                data_by_kab[kab][f"IPM_201{5+j}"] = val
            # 2020-2025 from table 2
            for j in range(6):
                val = clean_val(df.iloc[i, j+11])
                data_by_kab[kab][f"IPM_202{j}"] = val

    elif 'Umur Harapan Hidup' in csv_f:
        df = pd.read_csv(path, header=None)
        # Check structure from our earlier print:
        # col 1-6 is 2020-2025 table 1. col 7-16 is 2015-2024 table 2.
        y1 = [str(x) for x in df.iloc[1, 1:7].tolist()] # '2020', '2021.0'...
        y2 = [str(x) for x in df.iloc[1, 7:17].tolist()] # '2015', ...
        for i in range(2, len(df)):
            kab = standardize_name(df.iloc[i, 0])
            if kab not in data_by_kab: continue
            # Table 2 has 2015-2019
            for j in range(5):
                val = clean_val(df.iloc[i, j+7])
                data_by_kab[kab][f"UHH_201{5+j}"] = val
            # Table 1 has 2020-2025
            for j in range(6):
                val = clean_val(df.iloc[i, j+1])
                data_by_kab[kab][f"UHH_202{j}"] = val

    elif 'Produk Domestik Regional Bruto per Kapita' in csv_f:
        df = pd.read_csv(path, header=None)
        year_row_1 = df.iloc[2, 1:11].tolist()
        year_row_2 = df.iloc[2, 11:21].tolist()
        for i in range(3, len(df)):
            kab = standardize_name(df.iloc[i, 0])
            if kab not in data_by_kab: continue
            for j in range(10): # 2015-2024
                val1 = clean_val(df.iloc[i, j+1])
                val2 = clean_val(df.iloc[i, j+11])
                if val1 is not None: data_by_kab[kab][f"PDRB_ADHB_{2015+j}"] = round(val1 / 1000.0, 2)
                if val2 is not None: data_by_kab[kab][f"PDRB_ADHK_{2015+j}"] = round(val2 / 1000.0, 2)

    else:
        df = pd.read_csv(path, header=None)
        years_row = df.iloc[1, 1:].tolist()
        years = []
        for y in years_row:
            try: years.append(int(float(str(y))))
            except: years.append(None)
            
        indicator_name = "Indikator_Lain"
        if "Gini" in csv_f: indicator_name = "Gini"
        elif "Harapan Lama Sekolah" in csv_f: indicator_name = "HLS"
        elif "Pengeluaran Per Kapita" in csv_f: indicator_name = "Pengeluaran"
        elif "Persentase Penduduk Miskin" in csv_f: indicator_name = "Kemiskinan_Persen"
        elif "Jumlah Penduduk Miskin" in csv_f: indicator_name = "Kemiskinan_Jumlah"
        elif "Rata-Rata Lama Sekolah" in csv_f: indicator_name = "RLS"
        elif "Tingkat Pengangguran" in csv_f: indicator_name = "Pengangguran"
        elif "Laju Pertumbuhan" in csv_f: indicator_name = "Pertumbuhan_Ekonomi"

        for i in range(2, len(df)):
            kab = standardize_name(df.iloc[i, 0])
            if kab not in data_by_kab: continue
            for col_idx, y in enumerate(years):
                if y is not None:
                    val = clean_val(df.iloc[i, col_idx+1])
                    if val is not None:
                        data_by_kab[kab][f"{indicator_name}_{y}"] = val

# Inject properties into GeoJSON
for f in feature_kab:
    kab = f['properties']['std_name']
    for k, v in data_by_kab.get(kab, {}).items():
        f['properties'][k] = v

kab_fc = {
    "type": "FeatureCollection",
    "features": feature_kab
}

# Dummy data for Kecamatan
for f in feature_kec:
    for y in range(2015, 2026):
        f['properties'][f'Kemiskinan_Persen_{y}'] = round(random.uniform(2.0, 15.0), 2)
        f['properties'][f'IPM_{y}'] = round(random.uniform(60.0, 80.0), 2)
        f['properties'][f'Pertumbuhan_Ekonomi_{y}'] = round(random.uniform(-2.0, 7.0), 2)

kec_fc = {
    "type": "FeatureCollection",
    "features": feature_kec
}

print("Saving JS files...")
with open('sumbar-kabupaten-data.js', 'w', encoding='utf-8') as f:
    f.write("var statesData = " + json.dumps(kab_fc) + ";\n")

with open('sumbar-kecamatan-data.js', 'w', encoding='utf-8') as f:
    f.write("var kecamatanData = " + json.dumps(kec_fc) + ";\n")

print("Data processing complete!")
