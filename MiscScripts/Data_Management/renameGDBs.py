__author__ = 'WebbL'

import arcpy
from arcpy import env
import os




folder = r'\\uksapp03\Proj\Drainage\Data\Area04\Inventory_Data\Stage02\HADDMS'
#\\uksapp03\proj\Drainage\Data\Area04\Inventory_Data\Stage02\ADC   Stage01_ADC.gdb
#\\uksapp03\proj\Drainage\Data\Area04\Inventory_Data\Stage02\HADDMS Stage01_HADDMS.gdb


#folder = r'L:\Temp\LASTest'

env.workspace = folder

databases = arcpy.ListWorkspaces('*', 'FileGDB' )

for database in databases:
    head, tail = os.path.split(database)
    oldName =  tail
    #newDBName = tail[:-4] + "_HADDMS_Input.gdb"
    newDBName = oldName.replace('Stage01_HADDMS', '_Stage01_HADDMS')
    print newDBName

    arcpy.Rename_management(oldName, newDBName, "FileGDB")
