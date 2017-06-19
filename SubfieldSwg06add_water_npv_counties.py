# need to run this script for each county to clip water and rivers to the county boundaries



print("Running script ...")

import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

print("Importing water body and river feature classes ...")
print("")
# import other features into the database:
# water bodies
in_features = "C:/Users/ebrandes/Documents/geodata/dtl_wat.gdb/dtl_wat"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_name = "Waterbody"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)
# rivers
in_features = "C:/Users/ebrandes/Documents/geodata/dtl_riv.gdb/dtl_riv"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_name = "Rivers"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)

print("Reprojecting water body and river feature classes ...")
print("")
# reproject the feature classes
in_dataset = "Waterbody"
out_dataset = "Waterbody_NAD83"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system of " + str(out_dataset) + " is " + str(spatialRef.Name) +".")
print("")

# reproject the feature classes
in_dataset = "Rivers"
out_dataset = "Rivers_NAD83"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system of " + str(out_dataset) + " is " + str(spatialRef.Name) +".")
print("")


# make a feature layer from the county selected from the county feature class
in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
fips_select = "IA085"
out_layer = fips_select
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)


print("Clipping water body and river feature classes to " + str(fips_select) + "...")
print("")
# clip feature classes to watershed boundaries
in_features = "Waterbody_NAD83"
clip_features = out_layer
out_feature_class = "Waterbody_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# clip feature classes to watershed boundaries
in_features = "Rivers_NAD83"
out_feature_class = "Rivers_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# Clean up feature layers
arcpy.Delete_management(out_layer)

# make a feature layer from the county selected from the county feature class
in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
fips_select = "IA157"
out_layer = fips_select
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)


print("Clipping water body and river feature classes to " + str(fips_select) + "...")
print("")
# clip feature classes to watershed boundaries
in_features = "Waterbody_NAD83"
clip_features = out_layer
out_feature_class = "Waterbody_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# clip feature classes to watershed boundaries
in_features = "Rivers_NAD83"
out_feature_class = "Rivers_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# Clean up feature layers
arcpy.Delete_management(out_layer)

# make a feature layer from the county selected from the county feature class
in_features = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb\\Counties"
fips_select = "IA043"
out_layer = fips_select
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)


print("Clipping water body and river feature classes to " + str(fips_select) + "...")
print("")
# clip feature classes to watershed boundaries
in_features = "Waterbody_NAD83"
clip_features = out_layer
out_feature_class = "Waterbody_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# clip feature classes to watershed boundaries
in_features = "Rivers_NAD83"
out_feature_class = "Rivers_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# Clean up feature layers
arcpy.Delete_management(out_layer)



print("All done! :)")
