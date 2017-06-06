from collections import namedtuple
import json
import console
import ui

race = namedtuple('race', 'season round time raceName date url Circuit')
race_fmt = ('{round:>2} on {date}T{time} {raceName} at {Circuit[circuitName]}'
            ' in {Circuit[Location][locality]}, {Circuit[Location][country]}')

filename = 'current.json'

try:
    with open(filename) as in_file:
        data = json.load(in_file)
except FileNotFoundError:
    exit("Please run 'f1_get.py' before running this script.")

races = [race(**r) for r in data['MRData']['RaceTable']['Races']]
print(races[6])

class RaceView(ui.View):
    def __init__(self, races=races):
        self.name = f'Formula 1 - {races[0].season} raceing season'
        self.add_subview(self.make_races_view(races))

    def layout(self):
        self.subviews[0].frame = self.bounds
        """
        x, y, w, h = self.bounds
        half_w, half_h = w / 2, h / 2
        self.subviews[0].frame = x, y, half_w, half_h       # image
        self.subviews[1].frame = half_w, y, half_w, h       # map
        self.subviews[2].frame = x, half_h, half_w, half_h  # offers
        """

    def make_races_view(self, races):
        table_view = ui.TableView()
        races_list = [race_fmt.format(**race._asdict()) for race in races]
        table_view.data_source = lds = ui.ListDataSource(races_list)
        lds.font = ('<system-bold>', 10)
        table_view.row_height = 20
        table_view.delegate = self
        return table_view

    def tableview_did_select(self, tableview, section, row):
        console.hud_alert(tableview.data_source.items[row][27:])

RaceView(races).present()
