__author__ = 'WebbL'


class config_ADCS():
    """Stores useful information for ADCS toolset"""

    def __init__(self):

        #Source HA Lines
        self.AreaLines = r'\\uksapp03\proj\ADCS\Connections\ADCS_Live.sde\ADCS_Live.DBO.General_HA_South_AreaLines'
        #Fields to store whether we have received Data for Area Lines
        self.AreaLinesMatchedField = 'LAS_Matched_Recieved'
        self.AreaLinesUnMatchedField = 'LAS_Unmatched_Recieved'
        self.AreaLinesImageryField = 'Imagery_Recieved'


        #LAS Index Table
        self.MMS_LasIndex = r'\\uksapp03\proj\ADCS\Connections\ADCS_Live.sde\ADCS_Live.DBO.MMS_LAS_Index'

        #Imagery Index Table
        self.MMS_ImageryIndex = r'\\uksapp03\proj\ADCS\Connections\ADCS_Live.sde\ADCS_Live.DBO.MMS_Imagery_Index'
        self.MMS_ImageryPoints = r'\\uksapp03\proj\ADCS\Connections\ADCS_Live.sde\ADCS_Live.DBO.MMS_Imagery_Points_Source'
        self.MMS_ImageryRedactedPoints = r'\\uksapp03\proj\ADCS\Connections\ADCS_Live.sde\ADCS_Live.DBO.MMS_Imagery_Points_Redacted'




