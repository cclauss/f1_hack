import json
import ui

filename = 'current.json'


def data_path_to_str(data_path):  # ['a', 0, 'b'] --> [a][0][b]
    return f'[{"][".join(str(key) for key in data_path or [])}]'


def str_to_data_path(name=''):    # [a][0][b] --> ['a', 0, 'b']
    name = name.strip('[]').split('][')
    return [] if name == [''] else [int(s) if s.isdigit() else s for s in name]


class DataElementView(ui.View):
    def __init__(self, data_path, subview):
        self.name = data_path_to_str(data_path)
        self.add_subview(subview)

    @property
    def data_path(self):
        return str_to_data_path(self.name)

    def layout(self):
        self.subviews[0].frame = self.bounds

    def will_close(self):  # never gets called :-(
        print('will_close!!')


class DiscoverView(ui.View):
    def __init__(self, data, name=''):
        self.name = name or 'API Discovery'
        self.data = data
        self.views = []
        self.add_subview(self.make_view([]))

    @property
    def curr_data_path(self):
        for view in self.views:
            if view.on_screen:

                return view.data_path
        return []

    def data_at_data_path(self, data_path):
        data = self.data
        for key in data_path:
            data = data[key]
        return data

    def layout(self):
        if self.subviews:
            self.subviews[0].frame = self.bounds

    def make_dict_view(self, data, data_path):
        items = [f'{k} ({type(v).__name__}): {v}' for k, v in data.items()]
        lds = ui.ListDataSource(items)
        lds.font = ('<system-bold>', 10)
        table_view = ui.TableView(data_source=lds, delegate=self, row_height=20)
        return DataElementView(data_path=data_path, subview=table_view)

    def make_info_view(self, data, data_path):
        text_view = ui.TextView(text=f'{type(data).__name__}: {data}')
        return DataElementView(data_path=data_path, subview=text_view)

    def make_list_view(self, data, data_path):
        items = [f'{i} {item} ({type(item).__name__})' for i, item
                 in enumerate(data)]
        lds = ui.ListDataSource(items)
        lds.font = ('<system-bold>', 10)
        table_view = ui.TableView(data_source=lds, delegate=self, row_height=20)
        return DataElementView(data_path=data_path, subview=table_view)

    def make_view(self, data_path):
        data_path = data_path[:]  # make a local copy
        data = self.data_at_data_path(data_path)
        if isinstance(data, dict):
            return self.make_dict_view(data, data_path)
        elif isinstance(data, list):
            return self.make_list_view(data, data_path)
        else:
            return self.make_info_view(data, data_path)

    def tableview_did_select(self, tableview, section, row):
        key = tableview.data_source.items[row].split()[0]
        data_path = self.curr_data_path + [int(key) if key.isdigit() else key]
        view = self.make_view(data_path)
        self.views.append(view)
        tableview.navigation_view.push_view(view)

    def will_close(self):  # never gets called :-(
        print('will_close!!')


if __name__ == '__main__':
    print('=' * 23)
    try:
        with open(filename) as in_file:
            # json_discover('data', json.load(in_file))
            ui.NavigationView(DiscoverView(json.load(in_file))).present()
            # DiscoverView(json.load(in_file)).present()
    except FileNotFoundError:
        exit("Please run 'f1_get.py' before running this script.")
