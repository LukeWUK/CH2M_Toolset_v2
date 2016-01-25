__author__ = 'WebbL'

import os
import arcpy
from Library import LAZ_Decompress
import shutil
import sys
from ADCS.Config_ADCS import config_ADCS
from Library.Featureclass_Tools import lookup_values_using_key
from Library.Featureclass_Tools import does_value_exist

class createFinalLASDeliveryFolder():
    def __init__(self, inputFeatures, outputFolder,Road_Polygons):
        self.inputFeatures = inputFeatures
        self.outputFolder = outputFolder
        self.matchedOutputFolder = os.path.join(self.outputFolder, "Matched")
        self.unMatchedOutputFolder = os.path.join(self.outputFolder, "UnMatched")
        self.Road_Polygons = Road_Polygons

        self.LAS_ID_Field = "Filename"
        self.ADCS_Config = config_ADCS()
        self.Road_Polygons_ID_Field = "TEXTSTRING"

        self.main()


    def main(self):

        def createOutputFields():
            print "Creating Output Fields"
            try:
                arcpy.AddField_management(self.inputFeatures, "Matched_CopyQA", "TEXT", field_length=25)
                arcpy.AddField_management(self.inputFeatures, "UnMatched_CopyQA", "TEXT", field_length=25)
                arcpy.AddField_management(self.inputFeatures, "Polygon_CopyQA", "TEXT", field_length=25)
            except Exception as e:
                print ("Error Adding Fields: %s" % e)

        def copyMatched(LAS_Tile):
            srcPath = LAS_Tile.getValue("output_FolderPath")

            #Build variable list of potential input paths
            matchedFilepaths = []
            matchedFilepaths.append(srcPath)
            matchedFilepaths.append(srcPath.replace(".las", ".laz"))
            matchedFilepaths.append(srcPath.replace(".laz", ".las"))

            matchedFilepaths.append(srcPath.replace("\\B\\", "\\"))
            matchedFilepaths.append(srcPath.replace("\\B\\", "\\").replace(".laz", ".las"))
            matchedFilepaths.append(srcPath.replace("\\B\\", "\\").replace(".las", ".laz"))

            onDiskMatched = False
            for path in matchedFilepaths:
                if os.path.isfile(path):
                    onDiskMatched = True
                    filename = os.path.split(path)[1]
                    extension = os.path.splitext(path)[1]

                    outPath = os.path.join(self.matchedOutputFolder, filename[:-4]+ ".las")

                    if extension in (".las", ".LAS"):
                        print "Copying File: %s" % (path)
                        shutil.copyfile(path, outPath)
                    elif extension in (".laz", ".LAZ"):
                        output = LAZ_Decompress.decompressLAZ(path, outPath)
                        print "Decompressing File: %s" % (path)
                        print output
                    else:
                        print "Terminal Error %s" % (path)
                        sys.exit()
                    return True

            return False

        def copyUnmatched(LAS_Tile):
            #UnMatched
            #Accepted Unmatched LAS in DB
            whereClause = """   DataStatus = 0 and Type = 1           """

            rowID = LAS_Tile.getValue(self.LAS_ID_Field)
            filepaths = lookup_values_using_key(rowID,  self.ADCS_Config.MMS_LasIndex, self.LAS_ID_Field, "src_FolderPath" ,where=whereClause)
            onDiskUnMatched = False

            for filepath in filepaths:
                if os.path.isfile(filepath):
                    onDiskUnMatched = True
                    filename = os.path.split(filepath)[1]
                    #extension = os.path.splitext(filepath)[1]
                    outPath = os.path.join(self.unMatchedOutputFolder, filename[:-4]+ ".las")

                    print "Copying File: %s" % (filepath)
                    shutil.copyfile(filepath, outPath)
                    return True

            return False

        def createPolygon(LAS_Tile):
            filename = LAS_Tile.getValue(self.LAS_ID_Field)
            found, objectID = does_value_exist(filename, self.Road_Polygons, self.Road_Polygons_ID_Field)

            if found == True:

                whereClause = """  OBJECTID = %s      """ % (objectID)
                print "Creating Polygon"
                arcpy.Select_analysis(self.Road_Polygons, os.path.join(self.matchedOutputFolder, filename + ".shp" ), whereClause)
                return True

            return False


        createOutputFields()

        LAS_Tiles = arcpy.UpdateCursor(self.inputFeatures)

        for LAS_Tile in LAS_Tiles:
            print "Processing %s" %(LAS_Tile.getValue("Filename"))

            matchedFlag = copyMatched(LAS_Tile)
            unMatchedFlag = copyUnmatched(LAS_Tile)
            polygonFlag = createPolygon(LAS_Tile)

            LAS_Tile.setValue("Matched_CopyQA", matchedFlag)
            LAS_Tile.setValue("UnMatched_CopyQA", unMatchedFlag)
            LAS_Tile.setValue("Polygon_CopyQA", polygonFlag)

            LAS_Tiles.updateRow(LAS_Tile)

if __name__ == "__main__":
    inputFeatures = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Matched_LAS_Indexes\Area_4_A2'
    outputFolder = r'K:\ADCS\Areas\Area_4\A2\LidarFinal'
    Road_Polygons = r'L:\Projects\GIS\ADCS\DataDeliveryPrep\DataDeliveryPrep\DataDeliveryPrep.gdb\Road_Polygons'
    process = createFinalLASDeliveryFolder(inputFeatures, outputFolder, Road_Polygons)
    #t