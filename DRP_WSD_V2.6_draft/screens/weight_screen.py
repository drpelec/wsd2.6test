from kivy.lang import Builder
from screens.base import BaseScreen
from settings import DEVICES


Builder.load_file('screens/weight_screen.kv')


class WeightScreen(BaseScreen):

    def update_screen(self):
        super(WeightScreen, self).update_screen()
        weights = {d: self.app.state[d]['weight_wheel'] for d in DEVICES}
        total = sum(weights.values())
        self.ids.total_weight.set_value(total)
        if total > 0:
            self.ids.cross.set_value(round((weights['RF'] + weights['LR']) / total * 100., 1))
            self.ids.rs.set_value(round((weights['RF'] + weights['RR']) / total * 100., 1))
            self.ids.ls.set_value(round((weights['LF'] + weights['LR']) / total * 100., 1))
            self.ids.front.set_value(round((weights['RF'] + weights['LF']) / total * 100., 1))
            self.ids.rear.set_value(round((weights['RR'] + weights['LR']) / total * 100., 1))
        self.ids.total_front.set_value(weights['RF'] + weights['LF'])
        self.ids.bite.set_value(weights['LR'] - weights['RR'])
