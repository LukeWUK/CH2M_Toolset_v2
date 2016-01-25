__author__ = 'WebbL'



import arcpy
from arcpy import env
import os
from Library.Featureclass_Tools import lookup_values_using_key
from ADCS.Config_ADCS import config_ADCS


class flag_LAS_ifOnDisk():
    def __init__(self, LAS_Indexes):

        #Set Dynamic Params
        self.LAS_Indexes = LAS_Indexes

        #Set Static Params
        self.Flag_Matched_Field = "MatchedDataPresent"
        self.Flag_UnMatched_Field = "UnMatchedDataPresent"
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
                arcpy.AddField_management(os.path.join(self.LAS_Indexes, LAS_Index_FC), self.Flag_Matched_Field, "TEXT", field_length=254)
                arcpy.AddField_management(os.path.join(self.LAS_Indexes, LAS_Index_FC), self.Flag_UnMatched_Field, "TEXT", field_length=254)
            except Exception as e:
                print e


            cursor = arcpy.UpdateCursor(os.path.join(self.LAS_Indexes, LAS_Index_FC))

            whereClause = """   DataStatus = 0 and Type = 1           """

            for row in cursor:


                #Matched
                onDiskMatched = False
                filepathMatched = row.getValue("output_FolderPath")

                matchedFilepaths = []
                matchedFilepaths.append(filepathMatched)
                matchedFilepaths.append(filepathMatched.replace(".las", ".laz"))
                matchedFilepaths.append(filepathMatched.replace(".laz", ".las"))

                matchedFilepaths.append(filepathMatched.replace("\\B\\", "\\"))
                matchedFilepaths.append(filepathMatched.replace("\\B\\", "\\").replace(".laz", ".las"))
                matchedFilepaths.append(filepathMatched.replace("\\B\\", "\\").replace(".las", ".laz"))

                for path in matchedFilepaths:
                    if os.path.isfile(path):
                        onDiskMatched = True

                if onDiskMatched == False:
                    print filepathMatched

                #UnMatched
                rowID = row.getValue(self.LAS_ID_Field)
                filepaths = lookup_values_using_key(rowID,  self.ADCS_Config.MMS_LasIndex, self.LAS_ID_Field, "src_FolderPath" ,where=whereClause)
                onDiskUnMatched = False


                for filepath in filepaths:
                    #print filepath
                    if os.path.isfile(filepath):
                        onDiskUnMatched = True


                #Update Datasets
                row.setValue(self.Flag_Matched_Field, onDiskMatched)
                row.setValue(self.Flag_UnMatched_Field, onDiskUnMatched)

                cursor.updateRow(row)



if __name__ == "__main__":
    LAS_Indexes = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Matched_LAS_Indexes'
    process = flag_LAS_ifOnDisk(LAS_Indexes)