
import csv # for export into csv file
import sys # for export into csv file
import arcpy
import re # regular expression, to extract the cutoff values out of the scenario names

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"


# spatial join

target_features = "Townships_Projected"
join_features = "SubfieldIA_single"

SpatialJoin_analysis(target_features, join_features, out_feature_class, "JOIN_ONE_TO_MANY", \
                     "KEEP_ALL", "




in_dataset = "Townships"
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
desc = arcpy.Describe(out_dataset)
spatialRef = desc.SpatialReference
print("Just checking ... Reference System is " + str(spatialRef.Name) + ".")
