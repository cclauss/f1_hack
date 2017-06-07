from collections import namedtuple
import json
import console
import datetime
import ui

filename = 'current.json'
fields = 'season round time raceName date url Circuit'
race_data = namedtuple('race_data', fields)
race_fmt = ('{round:>2} on {date}T{time} {raceName} at {Circuit[circuitName]}'
            ' in {Circuit[Location][locality]}, {Circuit[Location][country]}')


def race_datetime(race):
    race_date = f"{race['date']}T{race['time']}"
    return datetime.datetime.strptime(race_date, '%Y-%m-%dT%H:%M:%SZ')


def in_the_future(race):  # supress races that are in the past
    four_hours = datetime.timedelta(hours=4)
    return race_datetime(race) + four_hours > datetime.datetime.utcnow()


class RacesView(ui.View):
    def __init__(self, races=races):
        self.name = f'Formula 1 - {races[0].season} racing season'
        self.add_subview(self.make_races_view(races))

    def layout(self):
        self.subviews[0].frame = self.bounds

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


if __name__ == '__main__':
    try:
        with open(filename) as in_file:
            data = json.load(in_file)
    except FileNotFoundError:
        exit("Please run 'f1_get.py' before running this script.")

    races = [race_data(**r) for r in data['MRData']['RaceTable']['Races']
             if in_the_future(r)]
    print(races[0])

    RacesView(races).present()
