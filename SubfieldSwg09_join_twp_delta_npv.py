
import arcpy
from arcpy import env
from arcpy.sa import *

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

print("Importing txt file into geodatabase ...")
print("")
# average delta NPV per township (table)
in_rows ="C:\\Users\\ebrandes\\Documents\\swg_econ\\manuscript\\tables\\delta_npv_twp.txt"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_table = "npv_twp"
#arcpy.TableToTable_conversion(in_rows, out_path, out_table)

# after this I manually added new fields (ending with _db) in which I copied the values
# that are saved as str into doubles, so that they can later be joined and worked with.
    
print("Importing township shapefile ...")
print("")
# import the required township shapefile into the file geodatabase
in_features = "C:/Users/ebrandes/Documents/geodata/shapefiles/political_townships.shp"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_name = "Townships"
#arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)

print("Reprojecting township feature class ...")
print("")
# reproject the feature class
in_dataset = out_name
out_dataset = str(out_name) + "_NAD83"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
#arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system is " + str(spatialRef.Name) +".")
print("")
print("Joining...")
print("")

# join the table containing delta NPV and twp id with the 
# feature class "Townships_NAD83"

in_feature_class = out_dataset
in_field = "POLITWP_ID"
join_table = out_table
join_field = "twp_db"
fields = ("delta_npv_db", "avg_delta_npv_db")
arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, fields)

print("Finito!")
