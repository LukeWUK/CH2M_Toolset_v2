__author__ = 'WebbL'



import arcpy
from arcpy import env
import os
from Library.Featureclass_Tools import does_value_exist
from ADCS.Config_ADCS import config_ADCS


class flag_LAS_WhereUnmatched():
    def __init__(self, LAS_Indexes):

        #Set Dynamic Params
        self.LAS_Indexes = LAS_Indexes

        #Set Static Params
        self.Flag_Field = "UnmatchedCheck"
        self.LAS_ID_Field = "Filename"

        self.ADCS_Config = config_ADCS()

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

            whereClause = """   DataStatus = 0 and Type = 1           """

            for row in cursor:
                rowID = row.getValue(self.LAS_ID_Field)
                found = does_value_exist(rowID,  self.ADCS_Config.MMS_LasIndex, self.LAS_ID_Field, where=whereClause)

                row.setValue(self.Flag_Field, found)
                cursor.updateRow(row)







if __name__ == "__main__":
    LAS_Indexes = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Matched_LAS_Indexes'
    process = flag_LAS_WhereUnmatched(LAS_Indexes)