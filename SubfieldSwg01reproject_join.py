# This is the first script run in the county specific yield cut-off analysis to identify target areas for switchgrass conversion.
# The 

import sys
print "Running script against: {}".format(sys.version)

# The argument noted below as sys.argv[1] is passed in the cmd script "SubfieldSwg01.cmd".
# It refers to the Iowa subfield feature class.

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

print("Reprojecting feature class " + str(sys.argv[1]) + " ...")

# reproject the feature class to NAD 83 UTM Zone 15N
# the feature class used here has already a field called
# cluid_mukey that will be used as unique identifyer for the join.
in_dataset = sys.argv[1]
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... spatial reference system is " + str(spatialRef.Name) +".")
print("Fields in feature class:")

# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name

print("Importing txt file into geodatabase ...")

# yield and cut off data (table)
in_rows ="C:\\Users\\ebrandes\\Documents\\swg_econ\\tables\\09_yields_cutoffs_2012_2015.txt"
out_path = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
out_name = "yields_2012_2015_cuts"
arcpy.TableToTable_conversion(in_rows, out_path, out_name)
    
print("Joining with corn/soybean yield and yield threshold data ...")

# join with corn yield data
in_feature_class = featureClass
in_field = "cluid_mukey" 
join_table = out_name
join_field = "cluid_mukey12"
field_list = ["fips", "crop12", "yield12", "crop13",
              "yield13", "crop14", "yield14", "crop15", "yield15", "cut_cg_min_16",
              "cut_sb_min_16", "cut_cg_2nd_16", "cut_sb_2nd_16", "cut_cg_min_6",
              "cut_sb_min_6", "cut_cg_2nd_6", "cut_sb_2nd_6"] 

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field_list)

# repair Geometry of feature class:
print("Repairing feature class geometry ...")
arcpy.RepairGeometry_management(in_feature_class)

# if MultipartToSinglepart does not work:
# e.g. ExecuteError: ERROR 000072: Cannot process feature with OID 822481:
# see script SubfieldSwg01delete_split_IDLE.py for a work-around.


print("Splitting multipart features ...")
# there are multipart polygons in the feature class that consist of one record (one cluid_mukey) but multiple polygons.
# Since we have to look at each polygon individually for its size and position in relation to others, we need to
# split all multipart polygons into singlepart polygons.
# The result is that there are duplicate records for some of the cluid_mukey records.
in_feature_class = featureClass
out_feature_class = str(in_dataset) + "_single"
arcpy.MultipartToSinglepart_management(in_feature_class, out_feature_class)
print("")
print("Done. Yippie!")





