##CERA2.0=group
##[CEro] Wave height inputs selection=name
##Study_area=vector
##Variable_wave_height=optional vector
##General_wave_height=optional number1
##Wave_height_classification=output vector

from qgis.core import *
from PyQt4.QtGui import QMessageBox

vwh = processing.getObject(Variable_wave_height)

if Variable_wave_height == None: #in case of being a general wave height
    if  General_wave_height != 0:
        processing.runalg('qgis:fieldcalculator', Study_area,'Hs',0,10.0,3.0,True,General_wave_height,Wave_height_classification)
    else: #in case of no valid input
        QMessageBox.warning(None, 'Optional features', 'At least one of the optional features is required')
else: #in case of using the layer
    field = 'Hs'
    index = vwh.fieldNameIndex(field)
    if index == -1:
        QMessageBox.warning(None, 'Attribute missing', 'Vector layer requires the wave height attribute to be named Hs')
    else:
        Wave_height_classification = Variable_wave_height