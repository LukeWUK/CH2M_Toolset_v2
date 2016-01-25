__author__ = 'WebbL'

import os
import arcpy
from arcpy import env


outputGDB = r'L:\Projects\GIS\ADCS\Drainage\HADDMS_Attributes\Data\Final_Data.gdb'

inputADC = os.path.join(outputGDB, "Input_ADC")
inputHADDMS = os.path.join(outputGDB, "Input_HADDMS")



#ADC
path = inputADC
env.workspace = path
inputLayers = arcpy.ListFeatureClasses('*')

#For each Input Layer
for layer in inputLayers:
    arcpy.CalculateField_management(os.path.join(path, layer), "Audit", '"Not Yet Considered"')


#HADDMS
path = inputHADDMS
env.workspace = path
inputLayers = arcpy.ListFeatureClasses('*')

#For each Input Layer
for layer in inputLayers:
    arcpy.CalculateField_management(os.path.join(path, layer), "Audit", '"Not Yet Considered"')