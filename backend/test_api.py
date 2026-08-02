import urllib.request, json

data = json.dumps({
    'steps': [
        {'reactant': '苯', 'product': '硝基苯', 'reagent': '浓HNO3/浓H2SO4'},
        {'reactant': '硝基苯', 'product': '苯胺', 'reagent': 'Fe/HCl'},
        {'reactant': '苯胺', 'product': '乙酰苯胺', 'reagent': '(CH3CO)2O'}
    ],
    'title': ''
}).encode()

req = urllib.request.Request(
    'http://localhost:8000/api/render/route-diagram',
    data=data,
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=30)
svg = resp.read().decode()

print('Status:', resp.status)
print('Size:', len(svg), 'bytes')

checks = [
    ('SimSun font', 'SimSun'),
    ('stroke-width 1.5', 'stroke-width="1.5"'),
    ('font-size 8 (label)', 'font-size="8"'),
    ('font-size 9 (reagent)', 'font-size="9"'),
    ('Times New Roman', 'Times New Roman'),
]
for label, pattern in checks:
    if pattern in svg:
        print(f'  [OK] {label}')
    else:
        print(f'  [MISSING] {label}')

# Save for inspection
with open('test_api_output.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print('Saved to test_api_output.svg')