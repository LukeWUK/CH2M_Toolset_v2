__author__ = 'WebbL'


#ID Fields
HADDMS_Fields = ['HADDMS_ID1', 'HADDMS_ID2', 'HADDMS_ID3', 'HADDMS_ID4', 'HADDMS_ID5', 'HADDMS_ID6', 'HADDMS_ID7', 'HADDMS_ID8', 'HADDMS_ID9']
ADC_Field = ["ADC_ID"]
OtherFields = ["CH_SOURCE", "Audit", "Audit_Detail" , "Catchment"]
allFields = HADDMS_Fields + ADC_Field + OtherFields

#Overlapping Assets dictionary
assetOverlaps = {}
case1 = ['manhole', 'catchpit', 'other_special_chamber', 'gully']
assetOverlaps['manhole'] =  case1
assetOverlaps['catchpit'] = case1
assetOverlaps['other_special_chamber'] = case1
del case1

assetOverlaps['gully'] = ['gully', 'catchpit']

case2 = ['surface_water_channel', 'combined_pipe_and_channel_drainage', 'drainage_channel_block']
assetOverlaps['surface_water_channel'] = case2
assetOverlaps['combined_pipe_and_channel_drainage'] = case2
assetOverlaps['drainage_channel_block'] = case2
del case2
#End Overlapping Assets dictionary


inferredDatasets = ['connector_node', 'pipework']
