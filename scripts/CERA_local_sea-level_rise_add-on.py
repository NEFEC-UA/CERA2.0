##CERA2.0=group
##[CEro] Local sea level rise add-on=name
##WCCR=vector
##Local_SLR=number
##Erosion_Potential=output vector

import math

slr_class = (Local_SLR <= 0) * 0 + (Local_SLR > 0 and Local_SLR <= 1) * 1 + (Local_SLR > 1 and Local_SLR <= 1.8) * 2 + (Local_SLR > 1.8 and Local_SLR <= 3) * 3 + (Local_SLR > 3) * 4

print slr_class

formula = 'round(("WCCRClass" + '+ str(slr_class) +' * 0.1) + 0.055)'
print formula

processing.runalg('qgis:fieldcalculator', WCCR,'EPClass',1,1.0,0.0,True,formula,Erosion_Potential)