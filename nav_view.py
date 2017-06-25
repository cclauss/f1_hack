import ui

class NavView(ui.View):
    def __init__(self, root_view, *args, **kwargs):
        self.root_view = root_view
        self.views = []
        self.push(root_view)

    def layout(self):
        for subview in  self.subviews:
            subview.frame = self.bounds

    def push(self, view):
        view.nav_view = self
        for subview in self.subviews:
            self.remove_subview(subview)
        self.add_subview(view)
        self.views.append(view)

    def pop(self):
        self.views.pop()
        for subview in self.subviews:
            self.remove_subview(subview)
        if self.views:
            self.add_subview(self.views[-1])

def action(sender):
    sender.nav_view.push(ui.Button(name='name', title='new'))
    

if __name__ == '__main__':
    print('=' * 23)
    NavView(ui.Button(name='name', title='title', action=action)).present()
