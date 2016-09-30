
import csv # for export into csv file
import sys # for export into csv file
import arcpy
import re # regular expression, to extract the cutoff values out of the scenario names

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"


# data needed:
# - feature class of subfield areas
# - feature class of township boundaries

 
# import shapefile into file database

#in_feature = "C:\\Users\\ebrandes\\Documents\\shapefiles\\political_townships.shp"
#out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
#out_name = "Townships"
#arcpy.FeatureClassToFeatureClass_conversion(in_feature, out_path, out_name)

# reproject feature class Townships

in_dataset = "Townships"
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
desc = arcpy.Describe(out_dataset)
spatialRef = desc.SpatialReference
print("Just checking ... Reference System is " + str(spatialRef.Name) + ".")
