import math
import re
import random

svg_file = r'C:\Users\theju\Pictures\thejuspk07\thejus_dark.svg'
with open(svg_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove existing neural-network group if present
content = re.sub(r'<g id="neural-network".*?>.*?</g>\n', '', content, flags=re.DOTALL)
content = re.sub(r'/\* NN_CSS_START \*/.*?/\* NN_CSS_END \*/', '', content, flags=re.DOTALL)

lines = []
nodes = []

layers = [
    {'x': 100, 'y_start': 100, 'y_step': 60, 'count': 5},
    {'x': 250, 'y_start': 70,  'y_step': 50, 'count': 7},
    {'x': 400, 'y_start': 130, 'y_step': 60, 'count': 4}
]

for i in range(len(layers) - 1):
    l1 = layers[i]
    l2 = layers[i+1]
    
    for n1 in range(l1['count']):
        y1 = l1['y_start'] + n1 * l1['y_step']
        for n2 in range(l2['count']):
            y2 = l2['y_start'] + n2 * l2['y_step']
            base_op = round(0.1 + 0.2 * (abs(math.sin(n1 * 1.3 + n2 * 2.1))), 2)
            high_op = min(1.0, base_op + 0.6)
            dur = round(2.0 + random.uniform(0, 3.0), 1)
            delay = round(random.uniform(0, 3.0), 1)
            
            line_str = f'<line x1="{l1["x"]}" y1="{y1}" x2="{l2["x"]}" y2="{y2}" stroke="#7DF9FF" stroke-width="1.5" opacity="{base_op}">'
            line_str += f'<animate attributeName="opacity" values="{base_op};{high_op};{base_op}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />'
            line_str += '</line>'
            lines.append(line_str)

for l in layers:
    for n in range(l['count']):
        y = l['y_start'] + n * l['y_step']
        # Inner solid node
        nodes.append(f'<circle cx="{l["x"]}" cy="{y}" r="5" fill="#00ff88" />')
        
        # Outer pulsating ring
        dur = round(1.5 + random.uniform(0, 1.5), 1)
        delay = round(random.uniform(0, 2.0), 1)
        
        node_str = f'<circle cx="{l["x"]}" cy="{y}" r="9" fill="none" stroke="#00ff88" stroke-width="1.5" opacity="0.6">'
        node_str += f'<animate attributeName="r" values="9;12;9" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />'
        node_str += f'<animate attributeName="opacity" values="0.6;0;0.6" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />'
        node_str += '</circle>'
        
        nodes.append(node_str)

equations = """
<text x="30" y="45" fill="#7DF9FF" font-size="12px" opacity="0.8">[ NEURAL_CORE :: ACTIVE ]</text>
<text x="120" y="420" fill="#00ff88" font-size="12px" opacity="0.6" font-style="italic">f(x) = 1 / (1 + e^-x)</text>
<text x="220" y="40" fill="#00ff88" font-size="12px" opacity="0.6" font-style="italic">L = -1/N ∑ (y_i log(ŷ_i))</text>
<text x="270" y="450" fill="#00ff88" font-size="12px" opacity="0.6" font-style="italic">a^(l) = g(W^(l) a^(l-1) + b^(l))</text>
<text x="40" y="400" fill="#7DF9FF" font-size="10px" opacity="0.5">C_t = f_t * C_{t-1} + i_t * \tilde{C}_t</text>
"""

nn_svg = "\n".join(lines) + "\n" + "\n".join(nodes) + "\n" + equations
nn_svg = f'<g id="neural-network" font-family="ConsolasFallback,Consolas,monospace">\n{nn_svg}\n</g>\n'

if '<text x="0" y="0">' in content:
    content = content.replace('<text x="0" y="0">', nn_svg + '<text x="0" y="0">')
    with open(svg_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully added ANIMATED neural network to SVG with EQUATIONS.')
else:
    print('Could not find text tag to inject into.')
