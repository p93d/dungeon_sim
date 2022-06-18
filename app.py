import dash
from dash.dependencies import Input, Output, State
import dash_daq as daq
from dash import dcc, html
import dash_bootstrap_components as dbc
from httplib2 import FailedToDecompressContent
import app_tools
import numpy as np




app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.DARKLY],
)

app.title = 'Dungeon Simulator'

server=app.server



fighter_class_inputs =  html.Div(
    [dbc.Label('Class')]+
    [dbc.Select(
        placeholder='Select Class...',
            options=[
                {"label": f"{_}", "value": f"{_}"} for _ in app_tools.class_names
            ],
            id=f"class_input_{i}"
    ) for i in range(6)]
)


health_inputs = html.Div(
    [dbc.Label('Health')] +
    [
    dbc.Input(
        id=f'health-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

defense_inputs = html.Div(
    [dbc.Label('Defense')] +
    [
        dbc.Input(
        id=f'defense-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

damage_inputs = html.Div(
    [dbc.Label('Damage')] +
    [
        dbc.Input(
        id=f'damage-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

crit_inputs = html.Div(
    [dbc.Label('Crit')] +
    [
        dbc.Input(
        id=f'crit-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

hit_inputs = html.Div(
    [dbc.Label('Hit')] +
    [
        dbc.Input(
        id=f'hit-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

dodge_inputs = html.Div(
    [dbc.Label('Dodge')] +
    [
        dbc.Input(
        id=f'dodge-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)


total_cost_labels = html.Div(
    [dbc.Label('Total Cost')] + 
    [dbc.InputGroupText(id=f'total_cost-output_{_}') for _ in range(6)]
)



"""
Inputs for items
"""
item_health_inputs = html.Div(
    [dbc.Label('Health')] +
    [
    dbc.Input(
        id=f'item_health-input_{_}',
        type='number',
        min=0,
        max=1000000,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

item_defense_inputs = html.Div(
    [dbc.Label('Defense')] +
    [
        dbc.Input(
        id=f'item_defense-input_{_}',
        type='number',
        min=0,
        max=100000,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

item_damage_inputs = html.Div(
    [dbc.Label('Damage')] +
    [
        dbc.Input(
        id=f'item_damage-input_{_}',
        type='number',
        min=0,
        max=250000,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

item_crit_inputs = html.Div(
    [dbc.Label('Crit')] +
    [
        dbc.Input(
        id=f'item_crit-input_{_}',
        type='text',
        value='0%',
        debounce=True

    ) for _ in range(6)]
)

item_hit_inputs = html.Div(
    [dbc.Label('Hit')] +
    [
        dbc.Input(
        id=f'item_hit-input_{_}',
        type='number',
        min=0,
        max=999999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

item_dodge_inputs = html.Div(
    [dbc.Label('Dodge')] +
    [
        dbc.Input(
        id=f'item_dodge-input_{_}',
        type='number',
        min=0,
        max=999999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

item_all_attr_inputs = html.Div(
    [dbc.Label('All Attr')] +
    [
        dbc.Input(
        id=f'item_all_attr-input_{_}',
        type='number',
        min=0,
        max=99999,
        value=0,
        debounce=True

    ) for _ in range(6)]
)

item_block_inputs = html.Div(
    [dbc.Label('Block %')] +
    [
        dbc.Input(
        id=f'item_block-input_{_}',
        type='text',
        value='0.0%',
        debounce=True

    ) for _ in range(6)]
)

item_dam_red_inputs = html.Div(
    [dbc.Label('DR %')] +
    [
        dbc.Input(
        id=f'item_dam_red-input_{_}',
        type='text',
        value='0.00%',
        debounce=True

    ) for _ in range(6)]
)


"""
Total Stats + Bonuses
"""
total_health_label = html.Div(
    [dbc.Label('Health')] + 
    [dbc.InputGroupText(id=f'total_health-output_{_}') for _ in range(6)]
)

total_defense_label = html.Div(
    [dbc.Label('Defense')] + 
    [dbc.InputGroupText(id=f'total_defense-output_{_}') for _ in range(6)]
)

total_damage_label = html.Div(
    [dbc.Label('Damage')] + 
    [dbc.InputGroupText(id=f'total_damage-output_{_}') for _ in range(6)]
)

total_crit_label = html.Div(
    [dbc.Label('Crit')] + 
    [dbc.InputGroupText(id=f'total_crit-output_{_}') for _ in range(6)]
)

total_hit_label = html.Div(
    [dbc.Label('Hit')] + 
    [dbc.InputGroupText(id=f'total_hit-output_{_}') for _ in range(6)]
)

total_dodge_label = html.Div(
    [dbc.Label('Dodge')] + 
    [dbc.InputGroupText(id=f'total_dodge-output_{_}') for _ in range(6)]
)


dungeon_level = dbc.Input(
    id='dungeon_level',
    type='number',
    min=126,
    max=9999,
    value=420,
    debounce=True
)



"""
Monster Stats
"""
monster_level_label = html.Div(
    [dbc.Label('Level')] + 
    [dbc.InputGroupText(id=f'monster_level-{_}') for _ in range(6)]
)

monster_health_label = html.Div(
    [dbc.Label('Health')] + 
    [dbc.InputGroupText(id=f'monster_health-{_}') for _ in range(6)]
)

monster_defense_label = html.Div(
    [dbc.Label('Defense')] + 
    [dbc.InputGroupText(id=f'monster_defense-{_}') for _ in range(6)]
)

monster_damage_label = html.Div(
    [dbc.Label('Damage')] + 
    [dbc.InputGroupText(id=f'monster_damage-{_}') for _ in range(6)]
)

monster_crit_label = html.Div(
    [dbc.Label('Crit')] + 
    [dbc.InputGroupText(id=f'monster_crit-{_}') for _ in range(6)]
)

monster_hit_label = html.Div(
    [dbc.Label('Hit')] + 
    [dbc.InputGroupText(id=f'monster_hit-{_}') for _ in range(6)]
)

monster_dodge_label = html.Div(
    [dbc.Label('Dodge')] + 
    [dbc.InputGroupText(id=f'monster_dodge-{_}') for _ in range(6)]
)





app.layout = dbc.Container([
    dcc.Store(id='fighter_values'),
    html.Br(),
    dbc.Button(
        "Show/Hide Stat Points",
        id="collapse-hard_stats-button",
        className="mb-3",
        color="secondary",
        n_clicks=0,
    ),

    ### Class Selection and Stat Allocation
    html.Div(
        dbc.Collapse([
            html.H4('Enter Stat Points'),
            html.P('First Fighter -> Top Right, Last Fighter -> Bottom Left', className='text-info'),
            dbc.Row([
                dbc.Col(fighter_class_inputs),
                dbc.Col(health_inputs),
                dbc.Col(defense_inputs),
                dbc.Col(damage_inputs),
                dbc.Col(crit_inputs),
                dbc.Col(hit_inputs),
                dbc.Col(dodge_inputs),
                dbc.Col(total_cost_labels),
            ]),            
            dbc.Label(id=f'total_investment'),
            html.Br()
            ],
            id="hard_stats-collapse",
            is_open=True,
        )
    ),


    # Item Stats
    dbc.Button(
        "Show/Hide Item Stats",
        id="collapse-item_stats-button",
        className="mb-3",
        color="secondary",
        n_clicks=0,
    ),
    html.Div(
        dbc.Collapse([
            html.H4('Enter Item Stats'),
            dbc.Row([
                dbc.Col(item_health_inputs),
                dbc.Col(item_defense_inputs),
                dbc.Col(item_damage_inputs),
                dbc.Col(item_crit_inputs),
                dbc.Col(item_hit_inputs),
                dbc.Col(item_dodge_inputs),
                dbc.Col(item_all_attr_inputs),
                dbc.Col(item_block_inputs),
                dbc.Col(item_dam_red_inputs),
            ]),
            html.Br(),],
            id="item_stats-collapse",
            is_open=True,
        )
    ),

    
    # Total Stats + Bonuses
    dbc.Button(
        "Show/Hide Total Stats",
        id="collapse-total_stats-button",
        className="mb-3",
        color="secondary",
        n_clicks=0,
    ),
    html.Div(
        dbc.Collapse([
            html.H4('Total Stats + Bonuses'),
            dbc.Row([
                dbc.Col(total_health_label),
                dbc.Col(total_defense_label),
                dbc.Col(total_damage_label),
                dbc.Col(total_crit_label),
                dbc.Col(total_hit_label),
                dbc.Col(total_dodge_label),
            ])],
            id="stats-collapse",
            is_open=False,
        )
    ),


    dbc.Label('Enter Dungeon Level:'),
    dbc.Col(dungeon_level, width=1),
    html.Br(),

    dbc.Button(
            "Show/Hide Monster Stats",
            id="collapse-monster_stats-button",
            className="mb-3",
            color="secondary",
            n_clicks=0,
    ),
    html.Div(
        dbc.Collapse([
            html.H4('Monster Stats'),
            dbc.Row([
                dbc.Col(monster_level_label),
                dbc.Col(monster_health_label),
                dbc.Col(monster_defense_label),
                dbc.Col(monster_damage_label),
                dbc.Col(monster_crit_label),
                dbc.Col(monster_hit_label),
                dbc.Col(monster_dodge_label),
            ]),
            html.Br()
        ],
        id="monsters-collapse",
        is_open=False,

        )
    ),

    dbc.Button(
        "Run Single Simulation", id="run_single_sim-button", className="me-2", n_clicks=0,
        ),
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Combat Log")),
                dbc.ModalBody(id='combat_output'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-body-scroll",
            scrollable=True,
            is_open=False,
            size='xl'
        ),

    dbc.Button(
        "Run 1000 Simulations", id="run_sim-button", className="me-2", n_clicks=0,
        ),
    dbc.Row([
    dbc.Label(id='sim_results')
    ]),
    dbc.Label('')
    
])



"""
Aggregating all Inputs/Outputs
"""
# Class Inputs
fighter_class_input_list = [
    f'class_input_{i}' for i in range(6)
]

total_cost_output_list = [
    f'total_cost-output_{i}' for i in range(6)
]


fighter_stat_names = [
    'health',
    'defense',
    'damage',
    'crit',
    'hit',
    'dodge'
]

item_stat_names = fighter_stat_names + [
        'all_attr',
        'block',
        'dam_red'
    ]


stat_input_list = [
    f'{s}-input_{i}' for s in fighter_stat_names for i in range(6)
]


item_stat_list = [
    f'item_{s}-input_{i}' for i in range(6) for s in item_stat_names   
]


total_stat_list = [
    f'total_{s}-output_{i}' for i in range(6) for s in fighter_stat_names 
]

monster_stat_list = [
    f'monster_{s}-{i}' for i in range(6) for s in fighter_stat_names
]

monster_level_list = [f'monster_level-{i}' for i in range(6)]



@app.callback(
    Output("stats-collapse", "is_open"),
    [Input("collapse-total_stats-button", "n_clicks")],
    [State("stats-collapse", "is_open")],
)
@app.callback(
    Output("monsters-collapse", "is_open"),
    [Input("collapse-monster_stats-button", "n_clicks")],
    [State("monsters-collapse", "is_open")],
)
@app.callback(
    Output("hard_stats-collapse", "is_open"),
    [Input("collapse-hard_stats-button", "n_clicks")],
    [State("hard_stats-collapse", "is_open")],
)
@app.callback(
    Output("item_stats-collapse", "is_open"),
    [Input("collapse-item_stats-button", "n_clicks")],
    [State("item_stats-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open




def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("run_single_sim-button", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)(toggle_modal)



"""
one mega callback
"""
@app.callback(
    [
        [Output(c, 'children') for c in total_cost_output_list],
        Output('total_investment', 'children'),
        [Output(s, 'children') for s in total_stat_list],
        Output('fighter_values', 'data')
    ],
    [
        [Input(x, 'value') for x in fighter_class_input_list],
        [Input(x, 'value') for x in stat_input_list],
        [Input(x, 'value') for x in item_stat_list],
    ]
)


def update_app(_fighter_classes, _stat_inputs, _item_stats):


    fighter_info_store = [[], [], [], [], [], []]

    # Determine number of unique classes
    unique_classes = []

    for c, fighter_class in enumerate(_fighter_classes):

        fighter_info_store[c].append(fighter_class)

        if fighter_class not in unique_classes:
            if fighter_class is not None:
                unique_classes.append(fighter_class)

    pct_bonus = 0.3 + .2*len(unique_classes)



    indiv_item_stats = np.array_split(_item_stats, 6)
    indiv_fighter_stats = [_stat_inputs[i::6] for i in range(6)]


    # Outputs
    cost_outputs = []
    stat_outputs = []
    total_cost = 0

    for _, (_fighter, _item) in enumerate(zip(indiv_fighter_stats, indiv_item_stats)):

        _fighter_cost = 0

        _item_all_attr = _item[6]

        for c, (_stat, _value) in enumerate(zip(_fighter, app_tools.stat_value(_fighter))):

            if _stat is not None:
                _fighter_cost+=sum([i*10000 for i in range(_stat+1)])

            if c != 3:
                stat_val = int(_value * (1+pct_bonus) + int(_item[c]) + int(_item_all_attr))
                stat_outputs.append(
                    f'{stat_val:,}'
                )
            else:
                stat_val = round(_value * (1+pct_bonus) + float(_item[c].strip('%'))/100, 4)
                stat_outputs.append(
                    str(round(stat_val*100,3))+'%'
                )

            fighter_info_store[_].append(stat_val)

        fighter_info_store[_].append(round(float(_item[7].strip('%'))/100,3))
        fighter_info_store[_].append(round(float(_item[8].strip('%'))/100,4))


        total_cost+=_fighter_cost
        cost_outputs.append(f'{int(_fighter_cost):,}')


    

    return cost_outputs, f'Total Investment: {int(total_cost):,}', stat_outputs, fighter_info_store






@app.callback(
    [
        [Output(m, 'children') for m in monster_stat_list],
        [Output(l, 'children') for l in monster_level_list],
    ],
    Input('dungeon_level', 'value')
)
def calc_monster_stats(dungeon_level):

    stat_outputs = []
    level_outputs = []

    for i in range(6):

        level_outputs.append(f'{dungeon_level - 25*i:,}')

        _monster_stats = app_tools.monster_stats(dungeon_level - 25*i)

        for c, _stat in enumerate(_monster_stats):

            if c != 3:

                stat_outputs.append(f'{_stat:,}')

            else:

                stat_outputs.append(f'{int(_stat*100)}%')

    return stat_outputs, level_outputs




@app.callback(
    Output('sim_results', 'children'),
    State('fighter_values', 'data'),
    State('dungeon_level', 'value'),
    Input('run_sim-button', 'n_clicks')
)
def run_sims(fighter_data, dung_level, clicks):

    _monsters = []

    for i in range(6):

        if dung_level - 25*i > 0:

            _monsters.append(app_tools.monster_stats(dung_level - 25*i))


    _fighters = [_fighter for _fighter in fighter_data if _fighter[0] is not None]


    num_wins = app_tools.sim_fight(_monsters, _fighters, num_sims=1000)
    
    return f'Sim Results:  {num_wins} wins, {1000-num_wins} losses ({round(num_wins/10,2)}%)'



@app.callback(
    Output('combat_output', 'children'),
    State('fighter_values', 'data'),
    State('dungeon_level', 'value'),
    Input('run_single_sim-button', 'n_clicks')
)
def run_sims(fighter_data, dung_level, clicks):

    _monsters = []

    for i in range(6):

        if dung_level - 25*i > 0:

            _monsters.append(app_tools.monster_stats(dung_level - 25*i))


    _fighters = [_fighter for _fighter in fighter_data if _fighter[0] is not None]

    
    return app_tools.sim_fight(_monsters, _fighters)






if __name__ == '__main__':
    
    app.run_server(debug=False)
