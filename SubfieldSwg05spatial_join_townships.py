
import csv # for export into csv file
import sys # for export into csv file
import arcpy
import re # regular expression, to extract the cutoff values out of the scenario names

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"


# make a feature layer from the feature classes "Test_SubfieldIA181_Selection" and "Test_Townships"

arcpy.MakeFeatureLayer_management("Test_SubfieldIA181_Selection", "test_subfield")
arcpy.MakeFeatureLayer_management("Test_Townships", "test_twp")

# select the features that cross township borders
in_layer = "test_subfield"
overlap_type = "CROSSED_BY_THE_OUTLINE_OF"
select_features = "test_twp"
arcpy.SelectLayerByLocation_management(in_layer, overlap_type, select_features)


# spatial join


