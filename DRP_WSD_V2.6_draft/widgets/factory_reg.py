# -*- coding: iso8859-15 -*-
from kivy.factory import Factory
from widgets.button import ImageButton, DRPButton
from widgets.card import Card
from widgets.checkbox import LabeledOption
from widgets.label import H1, H2, H3, H4, H6, P, ScrollableLabel, DRPIconLabel
from widgets.separator import Separator
from widgets.spinner import DRPSpinner
from widgets.wsd_item import WSDItem

Factory.register('WSDItem', cls=WSDItem)
Factory.register('LabeledOption', cls=LabeledOption)
Factory.register('H1', cls=H1)
Factory.register('H2', cls=H2)
Factory.register('H3', cls=H3)
Factory.register('H4', cls=H4)
Factory.register('H5', cls=H4)
Factory.register('H6', cls=H6)
Factory.register('P', cls=P)
Factory.register('ScrollableLabel', cls=ScrollableLabel)
Factory.register('ImageButton', cls=ImageButton)
Factory.register('DRPButton', cls=DRPButton)
Factory.register("DRPIconLabel", cls=DRPIconLabel)
Factory.register('Card', cls=Card)
Factory.register('Separator', cls=Separator)
Factory.register('WSDSpinner', cls=DRPSpinner)
