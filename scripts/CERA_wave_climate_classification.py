##CERA2.0=group
##[CEro] Wave climate classification=name
##Mean_wave_height=vector
##Number_of_storms=number
##Wave_climate_class=output vector

import math

storm_class = (Number_of_storms  == 0) * 1 + (Number_of_storms > 0 and Number_of_storms <= 5) *2 + (Number_of_storms > 5 and Number_of_storms <= 10) *3 + (Number_of_storms > 10 and Number_of_storms <= 15) *4 + (Number_of_storms > 15) *5

print storm_class

formula = 'round(sqrt("Hs class" * '+ str(storm_class) +') + 0.055)'
print formula

processing.runalg('qgis:fieldcalculator', Mean_wave_height,'ClimaClass',1,1.0,0.0,True,formula,Wave_climate_class)