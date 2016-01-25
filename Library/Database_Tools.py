__author__ = 'WebbL'




import arcpy
import os


def get_geodatabase_path(input_table):
  '''Return the Geodatabase path from the input table or feature class.
  :param input_table: path to the input table or feature class
  '''
  workspace = os.path.dirname(input_table)
  if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
    return workspace
  else:
    return os.path.dirname(workspace)


def lookupCodedValue(dataset, field, value):
    field = arcpy.ListFields(dataset, field)[0]
    if field.domain:
        domains = arcpy.da.ListDomains(get_geodatabase_path(dataset))
        for domain in domains:
            if domain.name == field.domain:
                return domain.codedValues[value]



def getCodedValueKey(dataset, field, value):
    field = arcpy.ListFields(dataset, field)[0]
    if field.domain:
        domains = arcpy.da.ListDomains(get_geodatabase_path(dataset))
        for domain in domains:
            if domain.name == field.domain:
                for key, val in domain.codedValues.iteritems():
                    if val == value:
                        return key



def lookupDomainValues(dataset, field):
    field = arcpy.ListFields(dataset, field)[0]
    if field.domain:
        domains = arcpy.da.ListDomains(get_geodatabase_path(dataset))
        for domain in domains:
            if domain.name == field.domain:
                return domain.codedValues


if __name__ == "__main__":
   dbLinesImagery = r'Database Connections\ADCS_Live.sde\ADCS_Live.DBO.MMS_Imagery_Index'
   print (lookupCodedValue(dbLinesImagery, 'HA_Area', 4))
   print (getCodedValueKey(dbLinesImagery, 'HA_Area', 'Area 4'))
