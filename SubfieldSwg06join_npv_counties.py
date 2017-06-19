# this script I join the NPV data from one table that includes all three selected counties:
# Harrison (IA085), Poweshiek (IA157), and Clayton (IA043)
# to each of the clipped feature classes

print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"


print("Importing txt file into geodatabase ...")

# yield and cut off data (table)
in_rows ="C:\\Users\\ebrandes\\Documents\\swg_econ\\manuscript\\tables\\npv_cty_select.txt"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_name = "npv_IA085_IA157_IA043"
arcpy.TableToTable_conversion(in_rows, out_path, out_name)
    
print("Joining IA085 with NPV data ...")

# join with corn yield data
in_feature_class = "clumu_IA085"
in_field = "object_id" 
join_table = out_name
join_field = "objectid"
fields = ("npv_rowcrops", "npv_swg", "d_npv")
#arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, fields)

print("")
print("Joining IA157 with NPV data ...")

# join with corn yield data
in_feature_class = "clumu_IA157"
in_field = "object_id" 
join_table = out_name
join_field = "objectid"
fields = ("npv_rowcrops", "npv_swg", "d_npv")
#arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, fields)

print("")
print("Joining IA043 with NPV data ...")

# join with corn yield data
in_feature_class = "clumu_IA043"
in_field = "object_id" 
join_table = out_name
join_field = "objectid"
fields = ("npv_rowcrops", "npv_swg", "d_npv")
arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, fields)

print("")
print("Done. Yippie!")

