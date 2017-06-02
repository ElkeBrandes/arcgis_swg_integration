
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


# check the spatial reference of the subfield polygon feature class
desc = arcpy.Describe("ia_clumu_2016_single")
spatialRef = desc.SpatialReference
print("Just checking ... Reference System of ia_clumu_2016_single is "
      + str(spatialRef.Name) + ".")
print("")

print("Making feature layers...")
print("")
# make feature layer from the subfield feature class
in_feature = "ia_clumu_2016_single"
out_layer = "subfield_layer"
arcpy.MakeFeatureLayer_management(in_feature, out_layer)

# make feature layer from township feature class
in_feature = "Townships_Projected"
out_layer = "township_layer"
arcpy.MakeFeatureLayer_management(in_feature, out_layer)

print("Selecting polygons that intersect with township borders...")
print("")
# select those polygons from the subfield feature layer that overlap with a township border
arcpy.SelectLayerByLocation_management("subfield_layer", "INTERSECT", "township_layer")

print("Saving selection as feature class...")
print("")
# save selection as feature class
in_features = "subfield_layer"
out_feature_class =  "twp_subfield_overlap"
arcpy.CopyFeatures_management(in_features, out_feature_class)

print("Intersecting...")
print("")
# intersect both feature classes
in_features = [out_feature_class, "Townships_Projected"]
out_feature_class = "twp_subfield_intersect"
arcpy.Intersect_analysis(in_features, out_feature_class)

print("Save intersect results as shapefile...")
print("")
# export the new feature class as a shapefile
output_folder = "C:/Users/ebrandes/Documents/geodata/shapefiles"
arcpy.FeatureClassToShapefile_conversion(out_feature_class, output_folder)
print("Fertig!")
