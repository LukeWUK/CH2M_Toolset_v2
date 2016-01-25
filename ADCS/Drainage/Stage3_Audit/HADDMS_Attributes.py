from ADCS.Drainage.Stage3_Audit import HADDMS_Attributes_Lookups

__author__ = 'WebbL'

import arcpy
from arcpy import env
import os, sys




class AmalgamationSourcePopulator():
    def __init__(self, inputGDB):

        #Set input Parameters
        self.inputGDB = inputGDB

        #Static Parameters
        self.outputGDB = r'L:\Projects\GIS\ADCS\Drainage\HADDMS_Attributes\Data\Final_Data.gdb'

        #Dynamic Parameters
        self.assetOverlaps = HADDMS_Attributes_Lookups.assetOverlaps
        self.HADDMS_Fields = HADDMS_Attributes_Lookups.HADDMS_Fields
        self.ADC_Field = HADDMS_Attributes_Lookups.ADC_Field
        self.OtherFields = HADDMS_Attributes_Lookups.OtherFields
        self.allFields = HADDMS_Attributes_Lookups.allFields
        self.inferredDatasets = HADDMS_Attributes_Lookups.inferredDatasets

        self.inputADC = os.path.join(self.outputGDB, "Input_ADC")
        self.inputHADDMS = os.path.join(self.outputGDB, "Input_HADDMS")
        self.outputInventory = os.path.join(self.outputGDB, "Initial_Inventory")
        self.outputInventoryRel = os.path.join(self.outputGDB, "ID_Relationships")
        self.tempFolder = os.path.join(self.outputGDB, "Temp")

        self.main()

    def main(self):
        env.workspace = self.inputGDB
        inputLayers = arcpy.ListFeatureClasses('*')

        #For each Input Layer
        for layer in inputLayers:
            ADC_Layers, HADDMS_Layers = self.findRequiredLayers(layer)
            self.updateGeodatabase(layer, ADC_Layers, HADDMS_Layers)
            print ""



    def getAssetName(self, input, dataSource):
        dataSources = {
            'Input_GDB': 3,
            'Input_ADC': 3,
            'Input_HADDMS': 2
        }

        if dataSource in dataSources:
            n=dataSources[dataSource]
            groups = input.split('_')
            return str('_'.join(groups[n:]).lower())
        else:
            print "Unable to find datasource for naming identification"
            sys.exit()

    def findRequiredLayers(self, layer):

        def GDB_Lookup(types, sourceDataset):

            #Get path to where we will search for layers
            if sourceDataset == "Input_ADC":
                path = self.inputADC
            elif sourceDataset == "Input_HADDMS":
                path = self.inputHADDMS
            else:
                print "Error in code"
                sys.exit()

            outLayers = []

            env.workspace = path
            possibleMatchLayers = arcpy.ListFeatureClasses('*')

            for possibleMatch in possibleMatchLayers:
                possibleMatchName = self.getAssetName(possibleMatch, sourceDataset)
                #print "Possible Match Name: %s    Datasource:  %s" % (possibleMatchName, sourceDataset)

                if possibleMatchName in types:
                    outLayers.append(possibleMatch)

            return outLayers

        print "Input Layer: %s" % (layer)

        inputLayerType = self.getAssetName(layer, "Input_GDB")
        print "Identified as : %s" % (inputLayerType)

        if inputLayerType in self.assetOverlaps:
            types = self.assetOverlaps[inputLayerType]
            print "Group Asset - Searching for Asset FCs: %s" % (types)
        else:
            types = [inputLayerType]
            print "Normal Asset - Searching for Asset FC: %s" % (types)


        ADC_Layers = GDB_Lookup(types, "Input_ADC")
        HADDMS_Layers = GDB_Lookup(types, "Input_HADDMS")

        print "ADC Matches Found: "

        for layer in ADC_Layers:
            print layer

        print "HADDMS Matches Found: "

        for layer in HADDMS_Layers:
            print layer



        return ADC_Layers, HADDMS_Layers

    def updateGeodatabase(self, layer, ADC_Layers, HADDMS_Layers):

        def identifyOrCreateOutputTable(layer):
            def createLayer(name, type, spaRef):
                arcpy.CreateFeatureclass_management(self.outputInventory, name, type, spatial_reference=spaRef)
                for field in self.allFields:
                    arcpy.AddField_management(os.path.join(self.outputInventory, name), field, "TEXT", field_length=254)

            outputLayerName =  self.getAssetName(layer, "Input_GDB")
            outputLayerPath = os.path.join(self.outputInventory, outputLayerName)
            if arcpy.Exists(outputLayerPath):
                print "Existing Layer found %s" % (outputLayerPath)
            else:
                print "Creating Layer: %s" % (outputLayerPath)
                desc = arcpy.Describe(os.path.join(self.inputGDB, layer))
                type = desc.shapeType
                spaRef = desc.spatialReference
                createLayer(outputLayerName, type, spaRef)

            return outputLayerPath

        def identifyOrCreateRelTable(layer):
            def createLayer(name, type, spaRef):
                arcpy.CreateFeatureclass_management(self.outputInventoryRel, name, type, spatial_reference=spaRef)
                for field in self.allFields:
                    arcpy.AddField_management(os.path.join(self.outputInventoryRel, name), field, "TEXT", field_length=254)

            outputLayerName =  "rel_" + self.getAssetName(layer, "Input_GDB")
            outputLayerPath = os.path.join(self.outputInventoryRel, outputLayerName)
            if arcpy.Exists(outputLayerPath):
                print "Existing Layer found %s" % (outputLayerPath)
            else:
                print "Creating Layer: %s" % (outputLayerPath)
                desc = arcpy.Describe(os.path.join(self.inputGDB, layer))
                type = "Polyline"
                spaRef = desc.spatialReference
                createLayer(outputLayerName, type, spaRef)

            return outputLayerPath

        def updateOutputTable(layer):
            #Add Catchment Info to Input Dataset
            try:
                arcpy.AddField_management(os.path.join(self.inputGDB, layer), "Catchment", "TEXT", field_length=254)
            except:
                print "Failed to Add to : %s" % (os.path.join(self.inputGDB, layer))

            #Calculate Catchment Name
            head, tail = os.path.split(self.inputGDB)
            n=3
            groups = tail.split('_')
            catchment =  str('_'.join(groups[:n]))
            arcpy.CalculateField_management(os.path.join(self.inputGDB, layer), "Catchment", '"' + catchment + '"')

            #Populate Audit Field in Input Dataset
            try:
                arcpy.AddField_management(os.path.join(self.inputGDB, layer), "Audit", "TEXT", field_length=254)
                arcpy.AddField_management(os.path.join(self.inputGDB, layer), "Audit_Detail", "TEXT", field_length=254)
            except:
                print "Failed to Add to : %s" % (os.path.join(self.inputGDB, layer))



        def calculateAudit(feature, ADC_Layers, layer):

            def does_feature_have_ADC_ID(feature):
                hasID = False
                for field in self.ADC_Field:
                    if feature.getValue(field) != None and feature.getValue(field).strip() != "":
                        hasID = True
                return hasID

            def does_feature_have_HADDMS_ID(feature):
                hasID = False
                for field in self.HADDMS_Fields:
                    try:
                        if feature.getValue(field) != None and feature.getValue(field).strip() != "":
                            hasID = True
                    except:
                        pass
                        #print "Skipped field: %s" % (field)
                return hasID

            def has_feature_moved(feature, ADC_Layers):

                has_moved = True

                featID = feature.getValue('ADC_ID')
                geometry = feature.shape

                whereClause = """  ADC_ID = '%s'     """ % (featID)


                #Setup Searchursor on src data
                for ADC_Layer in ADC_Layers:

                    testCur = arcpy.SearchCursor(os.path.join(self.inputADC, ADC_Layer), where_clause=whereClause)
                    for test in testCur:
                        test_geometry = test.shape
                        if geometry.equals (test_geometry):
                            has_moved = False

                    try:
                        del test, testCur
                    except:
                        pass

                return has_moved


            def is_feature_new(feature):
                isNew = False
                if feature.getValue("CH_Source") == "New":
                    isNew = True
                return isNew


            def is_feature_inferred(feature, layer):
                inferred = False

                name = self.getAssetName(layer,'Input_GDB')
                if name in self.inferredDatasets and feature.getValue("CH_Source") == "New":
                    inferred = True

                return inferred



            feature_has_ADCID = does_feature_have_ADC_ID(feature)
            feature_has_HADDMSID = does_feature_have_HADDMS_ID(feature)


            if feature_has_ADCID:
                feature_has_moved = has_feature_moved(feature, ADC_Layers)
            else:
                feature_has_moved = False

            feature_is_new = is_feature_new(feature)
            feature_is_inferred = is_feature_inferred(feature, layer)



            audit = "Not Calculated"
            audit_detail = "Not Calculated"



            #Case 1
            if not feature_has_moved and not feature_is_new \
                    and feature_has_ADCID and feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "Combined"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))


            #Case 2
            if not feature_has_moved and not feature_is_new \
                    and not feature_has_ADCID and feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "HADDMS"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))


            #Case 3
            if feature_has_moved and not feature_is_new \
                    and feature_has_ADCID and feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "Combined"
                    audit_detail = "2016 Combined Update"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))

            #Case 4
            if feature_has_moved and not feature_is_new \
                    and feature_has_ADCID and not feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "ADC"
                    audit_detail = "2016 ADC Update"

                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))

            #Case 5
            if not feature_has_moved and feature_is_new \
                    and not feature_has_ADCID and feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "Combined"
                    audit_detail = "2016 Combined Addition"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))

            #Case 6
            if not feature_has_moved and feature_is_new \
                    and not feature_has_ADCID and not feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "New"
                    audit_detail = "2016 New Addition"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))


            #Case 7
            if not feature_has_moved and not feature_is_new \
                    and feature_has_ADCID and not feature_has_HADDMSID \
                    and not feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "ADC"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))


            #Case 8
            if not feature_has_moved and  feature_is_new \
                    and not feature_has_ADCID and not feature_has_HADDMSID \
                    and feature_is_inferred:
                if audit == "Not Calculated":
                    audit = "New"
                    audit_detail = "2016 Inferred"
                else:
                    print ("DUPLICATE CASE IDENTIFIED %s  %s" % (audit, "Combined"))



            return audit, audit_detail


        def updateHADDMSTables(outputRow, audit, auditDetail, HADDMS_Layers, relCursor):
            if audit in ("Combined", "HADDMS"):

                #Get co-ordinate of current feature:
                Current_Coordinate = outputRow.Shape.centroid


                for HADDMS_Layer in HADDMS_Layers:
                    for field in self.HADDMS_Fields:
                        try:
                            if outputRow.getValue(field):
                                whereclause = """    HADDMS_ID1 =  '%s'   """ % (outputRow.getValue(field))
                                HADDMS_Cursor = arcpy.UpdateCursor(os.path.join(self.inputHADDMS, HADDMS_Layer), where_clause=whereclause)
                                #print "Creating Cursor: %s     %s " % (os.path.join(self.inputHADDMS, HADDMS_Layer), whereclause)
                                for HADDMS_Row in HADDMS_Cursor:
                                    HADDMS_Row.Audit = audit
                                    HADDMS_Cursor.updateRow(HADDMS_Row)

                                    feat = relCursor.newRow()
                                    Target_Coordinate = HADDMS_Row.Shape.centroid

                                    if Target_Coordinate != Current_Coordinate:
                                        array = arcpy.Array()
                                        array.add(Current_Coordinate)
                                        array.add(Target_Coordinate)
                                        polyline = arcpy.Polyline(array)
                                        feat.shape = polyline
                                        feat.Audit = "TEST"
                                        array.removeAll()

                                        relCursor.insertRow(feat)
                                        del feat

                                try:
                                    del HADDMS_Row, HADDMS_Cursor
                                except:
                                    pass

                        except Exception as e:
                            if field in ('HADDMS_ID6','HADDMS_ID7','HADDMS_ID8','HADDMS_ID9'):
                                pass
                            else:
                                print "Skipped field %s" %(field)
                                print e


        def updateADCTables(outputRow, audit, auditDetail, ADC_Layers, relCursor):
            if audit in ("Combined", "ADC"):
                Current_Coordinate = outputRow.Shape.centroid
                for ADC_Layer in ADC_Layers:
                    for field in self.ADC_Field:

                        try:
                            if outputRow.getValue(field):
                                whereclause = """    ADC_ID =  '%s'   """ % (outputRow.getValue(field))

                                ADC_Cursor = arcpy.UpdateCursor(os.path.join(self.inputADC, ADC_Layer), where_clause=whereclause)
                                #print "Creating Cursor: %s     %s " % (os.path.join(self.inputADC, ADC_Layer), whereclause)
                                for ADC_Row in ADC_Cursor:
                                    ADC_Row.Audit = audit
                                    ADC_Cursor.updateRow(ADC_Row)

                                    feat = relCursor.newRow()
                                    Target_Coordinate = ADC_Row.Shape.centroid

                                    if Target_Coordinate != Current_Coordinate:
                                        array = arcpy.Array()
                                        array.add(Current_Coordinate)
                                        array.add(Target_Coordinate)
                                        polyline = arcpy.Polyline(array)
                                        feat.shape = polyline
                                        feat.Audit = "TEST"
                                        array.removeAll()

                                        relCursor.insertRow(feat)
                                        del feat

                                try:
                                    del ADC_Row, ADC_Cursor
                                except:
                                    pass
                        except:
                            print "Skipped field %s" %(field)


        def createTempRelLayer(layer):
            def createLayer(name, type, spaRef):
                arcpy.CreateFeatureclass_management(self.tempFolder,  name, type, spatial_reference=spaRef)
                for field in self.allFields:
                    arcpy.AddField_management(os.path.join(self.tempFolder, name), field, "TEXT", field_length=254)

            outputLayerName =  "TempRel_" + layer
            outputLayerPath = os.path.join(self.tempFolder, outputLayerName)
            if arcpy.Exists(outputLayerPath):
                arcpy.Delete_management(outputLayerPath)


            print "Creating Layer: %s" % (outputLayerPath)
            desc = arcpy.Describe(os.path.join(self.inputGDB, layer))
            type = "Polyline"
            spaRef = desc.spatialReference
            createLayer(outputLayerName, type, spaRef)

            return outputLayerPath



        print "Updating Geodatabase"

        #Add catchment and empty Audit fields to input dataset
        updateOutputTable(layer)

        #print os.path.join(self.inputGDB, layer)
        outputCursor = arcpy.UpdateCursor(os.path.join(self.inputGDB, layer))

        rel_Layer_Path = createTempRelLayer(layer)
        rel_Cursor = arcpy.InsertCursor(rel_Layer_Path)

        for outputRow in outputCursor:
            #if outputRow.OBJECTID % 10 == 0:
                #print "Processing Feat: %d" %(outputRow.OBJECTID)
            #print ADC_Layers, layer
            audit, auditDetail = calculateAudit(outputRow, ADC_Layers, layer)
            updateHADDMSTables(outputRow, audit, auditDetail, HADDMS_Layers, rel_Cursor)
            updateADCTables(outputRow, audit, auditDetail, ADC_Layers, rel_Cursor)


            outputRow.audit = audit
            outputRow.audit_Detail = auditDetail
            outputCursor.updateRow(outputRow)

        del outputRow, outputCursor

        outputTablePath = identifyOrCreateOutputTable(layer)
        relTablePath = identifyOrCreateRelTable(layer)

        #Append Parameters
        inputLayer = [os.path.join(self.inputGDB, layer)]
        targetLayer = outputTablePath

        arcpy.Append_management(inputLayer, targetLayer, "NO_TEST")

        #Rel Append Parameters
        inputLayer = [os.path.join(self.tempFolder, "TempRel_"+ layer)]
        targetLayer = relTablePath

        arcpy.Append_management(inputLayer, targetLayer, "NO_TEST")







if __name__ == "__main__":
    inGDB = r'\\uksapp03\proj\Drainage\Data\Area04\A259\Stage03\A04_A259_10_Stage03.gdb'
    a = AmalgamationSourcePopulator(inGDB)



