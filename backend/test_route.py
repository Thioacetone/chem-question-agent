from structure_renderer import StructureRenderer

# 测试1: 4步单行路线
steps4 = [
    {'smiles': 'c1ccccc1', 'label': 'A', 'reagent': ''},
    {'smiles': 'O=[N+]([O-])c1ccccc1', 'label': 'B', 'reagent': '浓HNO3/浓H2SO4'},
    {'smiles': 'Nc1ccccc1', 'label': 'C', 'reagent': 'Fe/HCl'},
    {'smiles': 'CC(=O)Nc1ccccc1', 'label': 'D', 'reagent': '(CH3CO)2O'},
]
svg = StructureRenderer.render_route_diagram_svg(steps4)
with open('test_4steps.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print(f'4步路线: {len(svg)} bytes')

# 测试2: 6步2行路线
steps6 = [
    {'smiles': 'c1ccccc1', 'label': 'A', 'reagent': ''},
    {'smiles': 'O=[N+]([O-])c1ccccc1', 'label': 'B', 'reagent': '浓HNO3/浓H2SO4'},
    {'smiles': 'Nc1ccccc1', 'label': 'C', 'reagent': 'Fe/HCl'},
    {'smiles': 'CC(=O)Nc1ccccc1', 'label': 'D', 'reagent': '(CH3CO)2O'},
    {'smiles': 'O=[N+]([O-])c1ccc(C(=O)O)cc1', 'label': 'E', 'reagent': 'KMnO4/H+'},
    {'smiles': 'Nc1ccc(C(=O)O)cc1', 'label': 'F', 'reagent': 'Fe/HCl'},
]
svg = StructureRenderer.render_route_diagram_svg(steps6)
with open('test_6steps.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print(f'6步路线: {len(svg)} bytes')
print('Done')