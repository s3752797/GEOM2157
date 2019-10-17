## Major Project
## Geospatial Programming
## Athenee Teofilo - S3752797

import os ## To import functions needed for the task
from qgis.core import (QgsVectorLayer)
from qgis.PyQt.QtCore import (QVariant)
from qgis.PyQt import (QtGui)

## Location of the file to be retrived and use on the program
filepath = "H:/GP/MajorProject/InputData/"

## Assigned Shapefile names to the different input and output files to be used in the program
inputShapefileA = "Public_Toilets.shp"
inputShapefileB = 'Mel_Boundary.shp'
inputShapefileC = 'Suburbs.shp'
inputShapefileD = 'Bus_Stops.shp'
inputShapefileE = 'Prin_Bic.shp'
outputShapefileA= "Public_Toilet050.shp"
outputShapefileB= "Public_Toilet50100.shp"
outputShapefileC= "Public_Toilet100250.shp"
outputShapefileD= "Public_Toilet5075.shp"
outputShapefileE= "Nearest_GeneralPublicToilet.shp"
outputShapefileF= "Toilet_Wheelchair.shp"
outputShapefileG= "Toilet_baby.shp"
outputShapefileH= "Nearest_WheelchairAccess.shp"
outputShapefileI= "Nearest_BabyFacility.shp"
outputShapefileJ= "Public_Toilet250500.shp"
outputShapefileK= "Shortest_General.shp"

## Assigned file to the raster and vector files to be used in the program.
## The arrangement of the layers being added has effects on the ooutput map layout.
mbLayer = iface.addVectorLayer((filepath + inputShapefileB), inputShapefileA[:-4], "ogr")
suburbLayer = iface.addVectorLayer((filepath + inputShapefileC), inputShapefileA[:-4], "ogr")
footpathLayer = iface.addVectorLayer((filepath + inputShapefileE), inputShapefileA[:-4], "ogr")
bsLayer = iface.addVectorLayer((filepath + inputShapefileD), inputShapefileA[:-4], "ogr")

##The following statements are the Buffer tool parameters for project.
buffParams = {"INPUT": bsLayer, "DISTANCE": .0005, "SEGMENTS": 5, "END_CAP_STYPE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2, "DISSOLVE": True, "OUTPUT": filepath + outputShapefileA}
buffParams1 = {"INPUT": bsLayer, "DISTANCE": .0010, "SEGMENTS": 5, "END_CAP_STYPE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2, "DISSOLVE": True, "OUTPUT": filepath + outputShapefileB}
buffParams2 = {"INPUT": bsLayer, "DISTANCE": .0025, "SEGMENTS": 5, "END_CAP_STYPE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2, "DISSOLVE": True, "OUTPUT": filepath + outputShapefileC}
buffParams3 = {"INPUT": bsLayer, "DISTANCE": .00075, "SEGMENTS": 5, "END_CAP_STYPE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2, "DISSOLVE": True, "OUTPUT": filepath + outputShapefileD}
buffParams4 = {"INPUT": bsLayer, "DISTANCE": .005, "SEGMENTS": 5, "END_CAP_STYPE": 0, "JOIN_STYLE": 0, "MITER_LIMIT": 2, "DISSOLVE": True, "OUTPUT": filepath + outputShapefileJ}

## Statement that executes the buffer tool for every layer
processing.run("native:buffer", buffParams)
processing.run("native:buffer", buffParams1)
processing.run("native:buffer", buffParams2)
processing.run("native:buffer", buffParams3)
processing.run("native:buffer", buffParams4)
bs250500=iface.addVectorLayer((filepath + outputShapefileJ), "", "ogr")    ## statement that designate the location and name of the output file
bs100250=iface.addVectorLayer((filepath + outputShapefileC), "", "ogr")    ## statement that designate the location and name of the output file
bs50100=iface.addVectorLayer((filepath + outputShapefileB), "", "ogr")    ## statement that designate the location and name of the output file
ba5075=iface.addVectorLayer((filepath + outputShapefileD), "", "ogr")    ## statement that designate the location and name of the output file
bs050=iface.addVectorLayer((filepath + outputShapefileA), "", "ogr")    ## statement that designate the location and name of the output file

## Statement that executes the addition of the public toilet shapefile
ptLayer = iface.addVectorLayer((filepath + inputShapefileA), inputShapefileA[:-4], "ogr")

##The following statements are the Select by Attribute parameters for project.
selectAttParams = {"INPUT": ptLayer, "FIELD": "wheelchair", "OPERATOR": 0, "VALUE": "yes", "METHOD": 0}
processing.run("qgis:selectbyattribute", selectAttParams)

## Statement that shows the parameters and executes the Extracts the selected features to create a seperate layer
extractParams = {"INPUT": ptLayer, "OUTPUT":filepath + outputShapefileF}
processing.run("native:saveselectedfeatures", extractParams)
toil_wheelchair=iface.addVectorLayer((filepath + outputShapefileF), "", "ogr")   ## statement that designate the location and name of the output file

##The following statements are the Select by Attribute parameters for project.
selectAttParams = {"INPUT": ptLayer, "FIELD": "baby_facil", "OPERATOR": 0, "VALUE": "yes", "METHOD": 0}
processing.run("qgis:selectbyattribute", selectAttParams)

## Statement that shows the parameters and executes the Extracts the selected features to create a seperate layer
extractParams = {"INPUT": ptLayer, "OUTPUT":filepath + outputShapefileG}
processing.run("native:saveselectedfeatures", extractParams)
toil_baby=iface.addVectorLayer((filepath + outputShapefileG), "", "ogr")   ## statement that designate the location and name of the output file

#Nearest Neighbour tool parameter for the selection of the nearest neighbour
nearNeighParams = {"INPUT": bsLayer, "INPUT_FIELD": "Stop_Numbe", "TARGET": ptLayer, "TARGET_FIELD": "name", "MATRIX_TYPE": 0, "NEAREST_POINTS": 1, "OUTPUT": filepath + outputShapefileE}

## statement that executes the nearest neighbourhood tool to show the nearest neighbour that is accessible for the general public. 
processing.run("qgis:distancematrix", nearNeighParams)
nearNeighLayer=iface.addVectorLayer((filepath + outputShapefileE), "", "ogr")    ## statement that designate the location and name of the output file

#Nearest Neighbour tool parameter for the selection of the nearest neighbour
nearWheelchair = {"INPUT": bsLayer, "INPUT_FIELD": "Stop_Numbe", "TARGET": toil_wheelchair, "TARGET_FIELD": "name", "MATRIX_TYPE": 0, "NEAREST_POINTS": 1, "OUTPUT": filepath + outputShapefileH}

## statement that executes the nearest neighbourhood tool to show the nearest neighbour that is accessible for the wheelchair accessible
processing.run("qgis:distancematrix", nearWheelchair)
nearNeighLayer=iface.addVectorLayer((filepath + outputShapefileH), "", "ogr")    ## statement that designate the location and name of the output file

#Nearest Neighbour tool parameter for the selection of the nearest neighbour
nearBabyFacil = {"INPUT": bsLayer, "INPUT_FIELD": "Stop_Numbe", "TARGET": toil_baby, "TARGET_FIELD": "name", "MATRIX_TYPE": 0, "NEAREST_POINTS": 1, "OUTPUT": filepath + outputShapefileI}

## statement that executes the nearest neighbourhood tool to show the nearest neighbour that is accessible for the toilet with baby Facility
processing.run("qgis:distancematrix", nearBabyFacil)
nearNeighLayer=iface.addVectorLayer((filepath + outputShapefileI), "", "ogr")    ## statement that designate the location and name of the output file

#Shortest route parameters from an identified bus stop
shortGeneralParams = {"INPUT": footpathLayer, "STRATEGY": 0, "START_POINT": '144.93730890000,-37.81414802000[EPSG:4326]', "END_POINTS": nearNeighLayer, "OUTPUT": filepath + outputShapefileK}

## statement that executes the shortest route tool
processing.run('native:shortestpathpointtolayer', shortGeneralParams)
short_General=iface.addVectorLayer((filepath + outputShapefileK), "", "ogr") ## statement that designate the location and name of the output file

##Statement that assigns the layout variables to the corresponding map layers
layer1Layout=QgsProject.instance().mapLayersByName('Public_Toilets Mel_Boundary')
layer=layer1Layout[0]
layer2Layout=QgsProject.instance().mapLayersByName('Nearest_GeneralPublicToilet')
layerA=layer2Layout[0]
layer3Layout=QgsProject.instance().mapLayersByName('Nearest_WheelchairAccess')
layerB=layer3Layout[0]
layer4Layout=QgsProject.instance().mapLayersByName('Nearest_BabyFacility')
layerC=layer4Layout[0]

## The following statemente creates a new map layout to create a map which adds the layers into the map
project=QgsProject.instance()
manager=project.layoutManager()
layoutName='GProgrammingProject'
layouts_list=manager.printLayouts()

for layout in layouts_list:
        if layout.name() == layoutName:
                manager.removeLayout(layout)
layout=QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layoutName)
manager.addLayout(layout)

## Statement that specifies the boundaries of the map layout and other details such as the background, the scale of the map and position.
map=QgsLayoutItemMap(layout)
map.setRect(20, 20, 20, 20)
ms=QgsMapSettings()
ms.setLayers([layer])
rect=QgsRectangle(ms.fullExtent())
rect.scale(1.0)
ms.setExtent(rect)
map.setExtent(rect)
map.setBackgroundColor(QColor(255,255,255,0))
layout.addLayoutItem(map)
map.attemptMove(QgsLayoutPoint(5,20, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(180,180, QgsUnitTypes.LayoutMillimeters))

## Statement that adds and creates a legend for the layout and its specifications.
legend=QgsLayoutItemLegend(layout)
legend.setTitle("LEGEND:")
layerTree=QgsLayerTree()
layerTree.addLayer(layer)
layerTree.addLayer(layerA)
layerTree.addLayer(layerB)
layerTree.addLayer(layerC)
legend.model().setRootGroup(layerTree)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(210,150,QgsUnitTypes.LayoutMillimeters))

## Statement that adds and creates a scalebar for the layout and its specifications.
scalebar=QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Line Ticks Up')
scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
scalebar.setNumberOfSegments(4)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(0.5)
scalebar.setLinkedMap(map)
scalebar.setUnitLabel('km.')
scalebar.setFont(QFont('Century Gothic', 10))
scalebar.update()
layout.addLayoutItem(scalebar)
scalebar.attemptMove(QgsLayoutPoint(220,190,QgsUnitTypes.LayoutMillimeters))

## Statement that adds and creates a map title for the layout and its specifications.
title=QgsLayoutItemLabel(layout)
title.setText("PUBLIC TOILET IN  MELBOURNE")
title.setFont(QFont('Century Gothic', 20))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(190,20,QgsUnitTypes.LayoutMillimeters))

## Statement that adds and creates other text in the map and its specifications.
label = QgsLayoutItemLabel(layout)
label.setText("Submitted by: Athenee Teofilo")
label.setFont(QFont('Century Gothic', 10))
label.adjustSizeToText()
layout.addItem(label)
label.attemptMove(QgsLayoutPoint(220,30,QgsUnitTypes.LayoutMillimeters))

