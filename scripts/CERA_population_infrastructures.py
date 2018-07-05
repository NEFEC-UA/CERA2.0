##CERA2.0=group
##[CVal] Population + Infrastructures=name
##Infrastructures=raster
##Population_density=raster
##Infrastructures_Population=output raster

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

def calculator(layers, entries):
    formula = designformula(entries)
    [extent, width, height] = resultextent(layers)
    path = str(Infrastructures_Population)
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
        
def designformula(entries):
    formula = '(' + str(entries[0].ref) + ' * ' + str(entries[1].ref) + ')^(1/2) + 0.055'
    print formula
    return formula


# Get layer object
infrastructures = processing.getObject(Infrastructures)
population = processing.getObject(Population_density)

#Layer string and entries
layers = [infrastructures, population] #make a string of layers

entries = defineentries(layers) #make a string of entries for the calculator

#Compute SS value

result = calculator(layers,entries)