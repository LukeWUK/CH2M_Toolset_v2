__author__ = 'WebbL'


import arcpy
from arcpy import env
import os
from Library.Featureclass_Tools import does_value_exist


class flag_LAS_WherePolygons():
    def __init__(self, LAS_Indexes, Road_Polygons):

        #Set Dynamic Params
        self.LAS_Indexes = LAS_Indexes
        self.Road_Polygons = Road_Polygons

        #Set Static Params
        self.Flag_Field = "PolygonCheck"
        self.Road_Polygons_ID_Field = "TEXTSTRING"
        self.LAS_ID_Field = "Filename"

        self.main()

    def main(self):
        env.workspace = self.LAS_Indexes

        LAS_Index_FCs = arcpy.ListFeatureClasses('*')

        for LAS_Index_FC in LAS_Index_FCs:
            print LAS_Index_FC

            #Add output field
            try:
                arcpy.AddField_management(os.path.join(self.LAS_Indexes, LAS_Index_FC), self.Flag_Field, "TEXT", field_length=254)
            except:
                pass


            cursor = arcpy.UpdateCursor(os.path.join(self.LAS_Indexes, LAS_Index_FC))
            for row in cursor:
                rowID = row.getValue(self.LAS_ID_Field)
                found = does_value_exist(rowID, self.Road_Polygons, self.Road_Polygons_ID_Field)

                row.setValue(self.Flag_Field, found)
                cursor.updateRow(row)







if __name__ == "__main__":
    LAS_Indexes = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Matched_LAS_Indexes'
    Road_Polygons = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Road_Polygons'
    process = flag_LAS_WherePolygons(LAS_Indexes, Road_Polygons)