__author__ = 'WebbL'

import arcpy
import numpy
import arcpy.da



def get_unique_field_values(table, field, where=None):
    if where is None:
        where = "1=1"
        #j

    data = arcpy.da.TableToNumPyArray(table, [field], where_clause=where)
    return numpy.unique(data[field])




def does_value_exist(value, dataset, field, where=None):
    found = False

    if where is None:
        where = "1=1"

    cursor = arcpy.SearchCursor(dataset, where_clause=where)

    for row in cursor:
        if row.getValue(field) == value:
            found = True
            objectID = row.getValue("objectID")
            break
    try:
        del row, cursor
    except:
        pass

    if found == True:
        return True, objectID
    else:
        return False


def lookup_values_using_key(key, dataset, key_field, value_field,  where=None):
    if where is None:
        where = "1=1"
    outValues = []

    cursor = arcpy.SearchCursor(dataset, where_clause=where)
    for row in cursor:
        if row.getValue(key_field) == key:
            output = row.getValue(value_field)
            outValues.append(output)
    return outValues