# this script selects polygons based on a certain value in a column of the attribute table and exports the
# attribute table as a txt file.

print("Running script ...")

import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = r"C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"




print("Filtering out areas that to be converted to switchgrass ...")
# select polygons that are converted to switchgrass for a selected scenario
# create a layer with select features

# variables:
in_feature = "SubfieldIA_single"
out_layer = "SubfieldIA_swg_2nd_16"
where_clause = '"in_swg_2nd_16_10000_20" IS NOT NULL'

arcpy.MakeFeatureLayer_management(in_feature, out_layer, where_clause)

print("Exporting coordinates and attributes to text file ...")
# export coordinates and attribute values from that layer to an ASCII text file

# variables:
input_layer = out_layer
value_field_list = ["OBJECTID", "cluid", "cluid_mukey", "crop12", "crop13", "crop14", "crop15", "Shape_Area"]
delimiter = "SPACE"
output_ASCII_file = "SubfieldIA_swg_2nd_16.txt"

arcpy.ExportXYv_stats(input_layer, value_field_list, delimiter, output_ASCII_file, "ADD_FIELD_NAMES")


# clean up in memory layer
arcpy.Delete_management(input_layer)

print("Done. Yay!")

