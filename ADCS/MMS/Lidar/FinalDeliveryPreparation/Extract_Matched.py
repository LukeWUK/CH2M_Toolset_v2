__author__ = 'WebbL'


import arcpy
from Library.Featureclass_Tools import get_unique_field_values
from Library.Database_Tools import lookupCodedValue
import os
from ADCS.Config_ADCS import config_ADCS


class extractMatched_LAS():
    def __init__(self, HA_Area, outputFeatureDataset):

        #Set Dynamic Variables
        self.HA_Area = HA_Area
        self.outputFeatureDataset = outputFeatureDataset

        #Set Static Variables
        self.ADCS_Config = config_ADCS()


        self.main()

    def getRoads(self):
        """Look at the Input LAS Data for the supplied area, and get unique list of roads"""
        whereClause = """          HA_Area = %s              """ % (self.HA_Area)

        roads = get_unique_field_values(self.ADCS_Config.MMS_LasIndex, "Road", whereClause)

        return roads

    def exportRoad(self, road):
        """Export the Matched LAS Tiles for the road into the output feature dataset"""

        whereClause = """      HA_Area = %s and Road = %s and DataStatus = 0 and Type = 2   """ % (self.HA_Area, road)
        outputArea = lookupCodedValue(self.ADCS_Config.MMS_LasIndex, 'HA_Area', self.HA_Area).replace(" ", "_")
        outputRoad = lookupCodedValue(self.ADCS_Config.MMS_LasIndex, 'Road', road).replace(" ", "_")

        outputName = "%s_%s" % (outputArea, outputRoad)
        outputPath = os.path.join(self.outputFeatureDataset, outputName )

        print whereClause, outputPath

        if arcpy.Exists(outputPath) == False:

            arcpy.Select_analysis(self.ADCS_Config.MMS_LasIndex, outputPath, where_clause=whereClause)

    def main(self):

        roads = self.getRoads()

        for road in roads:
            self.exportRoad(road)





if __name__ == "__main__":
    outputFeatureDataset = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Matched_LAS_Indexes'

    #print "Run 1"
    #HA_Area = 0
    #extractMatched_LAS(HA_Area, outputFeatureDataset)

    print "Run 2"
    HA_Area = 6
    extractMatched_LAS(HA_Area, outputFeatureDataset)