##CERA2.0=group
##[CExp] Topography+SS_exact_value=name
##Expected_Storm_Surge_in_meters=number
##Topography=raster
##Topography_SS=output raster

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import *
from PyQt4.QtGui import QMessageBox
import os

#Formulae

def defineentry(layer): #function to attach a layer to an entry
    a = QgsRasterCalculatorEntry()
    a.ref = layer.name() + '@1'
    a.raster = layer
    a.bandNumber = 1
    return a

def defineentries(layers): #function to create a string of entries
    entries = []
    for layer in layers:
        entry = defineentry(layer)
        entries.append(entry)
    return entries
	        
def resultextent(layers):
    Xextent = layers[0].extent().xMaximum() - layers[0].extent().xMinimum()
    Yextent = layers[0].extent().yMaximum() - layers[0].extent().yMinimum()
    extent = layers[0].extent()
    width = 0
    height = 0
    for layer in layers:
        if Xextent > layer.extent().xMaximum() - layer.extent().xMinimum() and Yextent > layer.extent().yMaximum() - layer.extent().yMinimum():
            Xextent = layer.extent().xMaximum() - layer.extent().xMinimum()
            Yextent = layer.extent().yMaximum() - layer.extent().yMinimum()
            extent = layer.extent()
            print layer.name()
        else:
            pass
        if width < layer.width():
            width = layer.width()
        else:
            pass
        if height < layer.height():
            height = layer.height()
        else:
            pass
    return extent, width, height

def calculator(layers, entries, SS):
    formula = designformula(entries, SS)
    [extent, width, height] = resultextent(layers)
    path = str(Topography_SS)
    calc = QgsRasterCalculator(formula,
                               path,
                               'GTiff',
                               extent,
                               width,
                               height,
                               entries)
    calc.processCalculation()
    result = QgsRasterLayer(path,'Physical Vulnerability')
    if result.isValid():
        return result
    else:
        QMessageBox.warning(None, 'Coastal Risk Assessment', 'The output layer is not valid!')
        
def designformula(entries, SS):
    formula = '(' + str(entries[0].ref) + ' < 5 + ' + str(SS) + ') * 5 + (' + str(entries[0].ref) + ' < 10 + ' + str(SS) + ' AND ' + str(entries[0].ref) + ' >= 5 + ' + str(SS) + ') * 4 + (' + str(entries[0].ref) + ' < 20 + ' + str(SS) + ' AND ' + str(entries[0].ref) + ' >= 10 + ' + str(SS) + ') * 3 + (' + str(entries[0].ref) + ' < 30 + ' + str(SS) + ' AND ' + str(entries[0].ref) + ' >= 20 + ' + str(SS) + ') * 2 + (' + str(entries[0].ref) + ' >= 30 + ' + str(SS) + ') * 1'
    print formula
    return formula

def stormsurgeclass(SSurge):
    if SSurge < 0.5:
        return 0.5
    elif SSurge < 2.0:
        return 2
    elif SSurge < 3.5:
        return 3.5
    elif SSurge < 5:
        return 5
    else:
        return 6.5

# Get layer object
topography = processing.getObject(Topography)

#Layer string and entries
layers = [topography] #make a string of layers

entries = defineentries(layers) #make a string of entries for the calculator

#Compute SS value
SSN = float(Expected_Storm_Surge_in_meters)
print SSN
SS = int(SSN)
print SS

result = calculator(layers,entries, SS)