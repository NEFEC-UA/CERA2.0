##CERA2.0=group
##[CEro] Change rate test and classification=name
##ChangeRates=vector
##ChangeRates_class=output vector

from qgis.core import *
from PyQt4.QtGui import QMessageBox

vwh = processing.getObject(ChangeRates)

cr = processing.getObject(ChangeRates)
field = 'ChangeRate'
index = cr.fieldNameIndex(field)
formula = 'to_int(if(  "ChangeRate"  > 0.5, 1, if(  "ChangeRate"  > -0.5, 2, if(  "ChangeRate"  > -1.5, 3, if(  "ChangeRate"  > -2.5, 4, if(  "ChangeRate" <= -2.5, 5, NULL))))))'
print formula

if index == -1:
    QMessageBox.warning(None, 'Attribute missing', 'Vector layer requires the wave height attribute to be named ChangeRate')
else:
    processing.runalg('qgis:fieldcalculator', ChangeRates,'CRClass',1,1.0,0,True,formula,ChangeRates_class)