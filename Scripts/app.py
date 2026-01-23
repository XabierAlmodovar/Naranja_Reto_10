import itertools
import pandas as pd
from dash import Dash, html, dcc, callback_context, dash_table
from dash.dependencies import Input, Output, State

# --- Lista de colores ---
color_list = [
    '#FFFFFF', '#40E0D0', '#A57E62', '#5C2F83', '#462C0E', '#DFC8B2',
    '#800000', '#87CEFA', '#614051', '#FF00A8', '#000000', '#D3D3D3',
    '#C19A6B', '#00008B', '#BBE2AD', '#E65A5B', '#0000FF', '#153668',
    '#B94600', '#DEB24C', '#F29985', '#000081', '#666633', '#5F5E5E',
    '#164A0A', '#9A8176', '#ECE9D6', '#C7A2A2', '#D84936', '#BBA9E4',
    '#3B6968', '#FFD200', '#008000', '#86BE2D', '#C9C9C9', '#768597',
    '#B5A45F', '#0053A5', '#FAC4DB', '#D0455F', '#640B22', '#8E1D03',
    '#FDF7B2', '#B11730', '#B3832E', '#FAAA6E', '#C4DDCE', '#EBD6A7',
    '#BCD2E7', '#FFFF00', '#FFC0CB', '#808080', '#FFA500'
]

def pattern_name(c1, c2):
    return f"pattern_{c1}_{c2}"

all_combinations = [(a, b, pattern_name(a, b)) for a, b in itertools.combinations(color_list, 2)]

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2("Evaluador de combinación de colores con estampado"),
    html.Div("Se mostrarán todas las combinaciones posibles de dos colores y un estampado con ambos."),
    html.Br(),

    html.Div(id="combo-info", style={"fontSize":"20px", "marginBottom":"15px"}),

    html.Div([
        html.Div(id='color-a-box', style={'width':'150px','height':'80px','border':'1px solid #000','borderRadius':'6px','display':'inline-block','marginRight':'20px'}),
        html.Div(id='color-b-box', style={'width':'150px','height':'80px','border':'1px solid #000','borderRadius':'6px','display':'inline-block','marginRight':'20px'}),
        html.Div(id='pattern-box', style={'width':'150px','height':'80px','border':'1px solid #000','borderRadius':'6px','display':'inline-block'}),
    ], style={'marginBottom':'20px'}),

    html.Button('Sí combina', id='yes-btn', n_clicks=0, style={'marginRight':'10px'}),
    html.Button('No combina', id='no-btn', n_clicks=0),

    dcc.Store(id='index', data=0),
    dcc.Store(id='results', data=[]),

    html.Hr(),
    html.H3("Resultados finales"),
    dash_table.DataTable(
        id='results-table',
        columns=[
            {'name':'Color A', 'id':'color_a'},
            {'name':'Color B', 'id':'color_b'},
            {'name':'Estampado', 'id':'pattern'},
            {'name':'Combina (1/0)', 'id':'label'}
        ],
        data=[],
        style_cell={'textAlign':'center','padding':'6px'},
        page_size=20
    )
])

@app.callback(
    Output('combo-info', 'children'),
    Output('color-a-box', 'style'),
    Output('color-b-box', 'style'),
    Output('pattern-box', 'style'),
    Input('index', 'data')
)
def show_current_combo(idx):
    if idx >= len(all_combinations):
        return "Completado. Todas las combinaciones han sido evaluadas.", {}, {}, {}

    c1, c2, p = all_combinations[idx]

    return (
        f"Combinación {idx+1} de {len(all_combinations)}: {c1} + {c2} con estampado {p}",
        {'width':'150px','height':'80px','border':'1px solid #000','borderRadius':'6px','backgroundColor':c1},
        {'width':'150px','height':'80px','border':'1px solid #000','borderRadius':'6px','backgroundColor':c2},
        {'width':'150px','height':'80px','border':'1px solid #000','borderRadius':'6px','background':'repeating-linear-gradient(45deg, '+c1+' 0 10px, '+c2+' 10px 20px)'}
    )

@app.callback(
    Output('results', 'data'),
    Output('index', 'data'),
    Output('results-table', 'data'),
    Input('yes-btn', 'n_clicks'),
    Input('no-btn', 'n_clicks'),
    State('index', 'data'),
    State('results', 'data')
)
def record_answer(yes, no, idx, results):
    ctx = callback_context
    if not ctx.triggered or idx >= len(all_combinations):
        return results, idx, results

    button = ctx.triggered[0]['prop_id'].split('.')[0]
    label = 1 if button == 'yes-btn' else 0
    c1, c2, p = all_combinations[idx]

    results = results.copy()
    results.append({'color_a': c1,'color_b': c2,'pattern': p,'label': label})

    # Guardar cada fila en CSV inmediatamente
    pd.DataFrame(results).to_csv('../Datos/Transformados/resultados_combinaciones.csv', index=False)

    return results, idx + 1, results

if __name__ == '__main__':
    app.run(debug=True)
