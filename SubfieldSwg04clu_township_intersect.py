
import csv # for export into csv file
import sys # for export into csv file
import arcpy
import re # regular expression, to extract the cutoff values out of the scenario names

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"


# data needed:
# - feature class of subfield areas
# - feature class of township boundaries

 
# import township shapefile into file database

in_feature = "C:\\Users\\ebrandes\\Documents\\geodata\\shapefiles\\political_townships.shp"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "Townships"
arcpy.FeatureClassToFeatureClass_conversion(in_feature, out_path, out_name)

# reproject feature class Townships

in_dataset = "Townships"
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
desc = arcpy.Describe(out_dataset)
spatialRef = desc.SpatialReference
print("Just checking ... Reference System of feature class " + str(out_dataset) +
      "  is " + str(spatialRef.Name) + ".")
print("")


print("Importing clu feature class ...")
print("")
# import cluid layer from the clu_ia database
in_features = "C:/Users/ebrandes/Documents/geodata/clu_ia.gdb/clu"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "CLU"
arcpy.FeatureClassToFeatureClass_conversion(in_features, out_path, out_name)

# check the spatial reference of the clu polygon feature class
desc = arcpy.Describe("CLU")
spatialRef = desc.SpatialReference
print("Just checking ... Reference System of CLU is "
      + str(spatialRef.Name) + ".")
print("")
print("projecting CLU features to NAD 1983...")
print("")
in_dataset = "CLU"
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the clu polygon feature class
desc = arcpy.Describe("CLU_Projected")
spatialRef = desc.SpatialReference
print("Just checking ... Reference System of CLU is "
      + str(spatialRef.Name) + ".")
print("")



print("Making feature layers...")
print("")
# make feature layer from the subfield feature class
in_feature = "CLU_Projected"
out_layer = "clu_layer"
arcpy.MakeFeatureLayer_management(in_feature, out_layer)

# make feature layer from township feature class
in_feature = "Townships_Projected"
out_layer = "township_layer"
arcpy.MakeFeatureLayer_management(in_feature, out_layer)

print("Selecting polygons that overlap with township borders...")
print("")
# select those polygons from the subfield feature layer that overlap with a township border
arcpy.SelectLayerByLocation_management("clu_layer", "CROSSED_BY_THE_OUTLINE_OF", "township_layer")

print("Saving selection as feature class...")
print("")
# save selection as feature class
in_features = "clu_layer"
out_feature_class =  "twp_clu_overlap"
arcpy.CopyFeatures_management(in_features, out_feature_class)

print("Intersecting...")
print("")
# intersect both feature classes
in_features = [out_feature_class, "Townships_Projected"]
out_feature_class = "twp_clu_intersect"
arcpy.Intersect_analysis(in_features, out_feature_class)

print("Exporting coordinates and attributes to text file ...")
# export coordinates and attribute values from that layer to an ASCII text file

# variables:
input_layer = out_feature_class
value_field_list = ["OBJECTID", "cluid", "POLITWP_ID", "SHAPE_Area"]
delimiter = "SPACE"
output_ASCII_file = "twp_clu_overlap.txt"
arcpy.ExportXYv_stats(input_layer, value_field_list, delimiter, output_ASCII_file, "ADD_FIELD_NAMES")

print("Selecting polygons that are fully within township borders...")
print("")
# select those polygons from the subfield feature layer that overlap with a township border
arcpy.SelectLayerByLocation_management("clu_layer", "COMPLETELY_WITHIN", "township_layer")

print("Saving selection as feature class...")
print("")
# save selection as feature class
in_features = "clu_layer"
out_feature_class =  "twp_clu_within"
arcpy.CopyFeatures_management(in_features, out_feature_class)

print("Intersecting...")
print("")
# intersect both feature classes
in_features = [out_feature_class, "Townships_Projected"]
out_feature_class = "twp_clu_intersect_within"
arcpy.Intersect_analysis(in_features, out_feature_class)

print("Exporting coordinates and attributes to text file ...")
# export coordinates and attribute values from that layer to an ASCII text file

# variables:
input_layer = out_feature_class
value_field_list = ["OBJECTID", "cluid", "POLITWP_ID",  "SHAPE_Area"]
delimiter = "SPACE"
output_ASCII_file = "twp_clu_within.txt"
arcpy.ExportXYv_stats(input_layer, value_field_list, delimiter, output_ASCII_file, "ADD_FIELD_NAMES")

print("Fertig!")
