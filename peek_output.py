import json
import ast

def peek(filepath):
    print(f"\n--- Peeking into {filepath} ---")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip the variable declaration 'var statesData = '
    json_str = content[content.find('= ')+2 : content.rfind(';')]
    data = json.loads(json_str)
    
    features = data.get('features', [])
    print(f"Total features: {len(features)}")
    
    if features:
        sample_feature = features[0]
        print(f"Sample Feature Properties for {sample_feature['properties'].get('name')}:")
        props = sample_feature['properties']
        prop_keys = list(props.keys())
        print(f"Number of properties: {len(prop_keys)}")
        
        # Print a few data points
        print("Sampel Data:")
        for key in ['IPM_2020', 'UHH_2022', 'PDRB_ADHB_2020', 'Kemiskinan_Persen_2024', 'Pertumbuhan_Ekonomi_2020']:
            if key in props:
                print(f"  {key}: {props[key]}")
            else:
                # Find a matching key that's close
                matches = [k for k in prop_keys if key.split('_')[0] in k]
                if matches:
                    print(f"  {matches[0]}: {props[matches[0]]}")
                else:
                    print(f"  {key} not found")
        
        # Find any Nulls
        nulls = {k: v for k, v in props.items() if v is None}
        print(f"Null values in sample: {len(nulls)}")

peek('sumbar-kabupaten-data.js')
peek('sumbar-kecamatan-data.js')
