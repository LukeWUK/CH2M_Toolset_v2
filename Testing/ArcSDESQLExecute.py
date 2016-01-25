__author__ = 'WebbL'


import arcpy

# Use a connection file to create the connection
egdb = r'K:\ADCS\Connections\ADCS_Live.sde'
egdb_conn = arcpy.ArcSDESQLExecute(egdb)

table_name = 'ADCS_Live.DBO.MMS_Imagery_Index'
field_name = 'CH2_ImgID'

sql = '''
SELECT {0}, COUNT({0}) AS f_count FROM {1}
GROUP BY {0}
ORDER BY f_count DESC
'''.format(field_name, table_name)

egdb_return = egdb_conn.execute(sql)
for i in egdb_return:
    print('{}: {}'.format(*i))