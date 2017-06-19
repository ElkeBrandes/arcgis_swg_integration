
import arcpy
from arcpy import env
from arcpy.sa import *

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"


print("Importing table...")
print("")

# import the table created in R that contains a list of all cluid and the townships they fall into

in_table = "C:/Users/ebrandes/Documents/swg_econ/manuscript/tables/clu_twp.txt"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_name = "clu_twp"
arcpy.TableToTable_conversion(in_table, out_path, out_name)



print("Joining...")
print("")

# join the table containing cluid and the associated township id with the 
# feature class "SubfieldIA_single"

in_feature_class = "SubfieldIA_single"
in_field = "cluid"
join_table = out_name
join_field = in_field
field = "twp"
arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field)

print("Filtering out areas that were not in corn/soybean 2012-2015 ...")
# select polygons that are in corn and soybeans
# create a layer with select features

# variables:
in_feature = "SubfieldIA_single"
out_layer = "SubfieldIA_single"
where_clause = '"crop12" IS NOT NULL'

arcpy.MakeFeatureLayer_management(in_feature, out_layer, where_clause)

print("Exporting coordinates and attributes to text file ...")
# export coordinates and attribute values from that layer to an ASCII text file

# variables:
input_layer = out_layer
value_field_list = ["object_id", "Shape_Area", "twp", "in_swg_2nd_16_10000_20"]
delimiter = "SPACE"
output_ASCII_file = "SubfieldIA_all.txt"

arcpy.ExportXYv_stats(input_layer, value_field_list, delimiter, output_ASCII_file, "ADD_FIELD_NAMES")


# clean up in memory layer
arcpy.Delete_management(input_layer)




print("Finito!")
