##CERA2.0=group
##Delete NULL features=name
##Layer=vector

from qgis.core import *

lyr = processing.getObject(Layer)
expression = '"ClimaClass" IS NULL OR "CRClass" IS NULL'

#checks
print lyr
print expression


with edit(lyr):
    # build a request to filter the features based on an attribute
    request = QgsFeatureRequest().setFilterExpression(expression)

    # we don't need attributes or geometry, skip them to minimize overhead.
    # these lines are not strictly required but improve performance
    request.setSubsetOfAttributes([])
    request.setFlags(QgsFeatureRequest.NoGeometry)

    # loop over the features and delete
    for f in lyr.getFeatures(request):
        lyr.deleteFeature(f.id())