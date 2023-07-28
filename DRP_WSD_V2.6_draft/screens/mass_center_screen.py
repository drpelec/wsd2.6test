from kivy.lang import Builder
from screens.base import BaseScreen
from settings import DEVICES
from widgets.label import P


Builder.load_file('screens/mass_center_screen.kv')


class CenterOfMassScreen(BaseScreen):

    def on_enter(self, *args):
        super(CenterOfMassScreen, self).on_enter(*args)
        for n in range(0, 110, 10):
            self.ids.box.add_widget(P(text=str(n), size_hint=(None, None), size=(25, 25),
                                      pos_hint={'center_x': n / 100., 'center_y': -.03}))
        for n in range(100, 0, -10):
            self.ids.box.add_widget(P(text=str(n), size_hint=(None, None), size=(25, 25),
                                      pos_hint={'center_y': n / 100., 'center_x': -.05}, halign='right'))

    def update_screen(self):
        super(CenterOfMassScreen, self).update_screen()
        w = {d: self.app.state[d]['weight_wheel'] for d in DEVICES}
        total = sum(w.values())
        if total > 0:
            self.ids.dot.opacity = 1
            left = round((w['LF'] + w['LR']) / total * 100., 1)
            right = round((w['RF'] + w['RR']) / total * 100., 1)
            front = round((w['RF'] + w['LF']) / total * 100., 1)
            rear = round((w['RR'] + w['LR']) / total * 100., 1)
            self.ids.lb_dot.text = '{}  {}'.format(right, front)
            self.ids.dot.pos_hint = {
                'center_x': right / 100.,
                'center_y': front / 100. - .03
            }
            self.ids.total.set_value(round(total, 2))
            self.ids.left.set_value(left)
            self.ids.right.set_value(right)
            self.ids.front.set_value(front)
            self.ids.rear.set_value(rear)
            self.ids.cross.set_value(round((w['RF'] + w['LR']) / total * 100., 1))
            self.ids.bite.set_value(w['LR'] - w['RR'])
        else:
            self.ids.dot.opacity = 0
