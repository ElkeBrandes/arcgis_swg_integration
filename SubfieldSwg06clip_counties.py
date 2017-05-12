# in this script, the feature class SubfieldIA_single that includes the four yield cut off scenarios is clipped to
# single counties to be able to zoom into the pattern of subfield switchgrass areas

print("Running script ...")

import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# make a feature layer from the county selected from the county feature class
in_features = "Counties"
out_layer = "IA085_Harrison"
fips_select = "IA085"
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)


# clip the subfield feature class to the selected county boundaries

in_features = "SubfieldIA_single"
clip_features = out_layer
out_feature_class = "SubfieldIA085"
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)



 
