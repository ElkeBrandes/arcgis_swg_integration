import sys
print "Running script against: {}".format(sys.version)

# enter parameters:
arg1 =  "SubfieldIA"
arg2 = "CornYields2011_2014"

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "E:\\switchgrass_integration.gdb"

print("Reprojecting feature class " + str(arg1) + " ...")

# reproject the feature class to NAD 83 UTM Zone 15N
in_dataset = arg1
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
    
print("Joining with corn yield data ...")

# join with corn yield data
in_feature_class = featureClass
in_field = "cluid_mukey" 
join_table = arg2
join_field = "cluid_mukey"
field_list = ["mean_corn_yield", "clumuha"]  # is "clumuha" needed?

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field_list)

# MultipartToSinglepart does not work: ExecuteError: ERROR 000072: Cannot process feature with OID 822481
# This is a strange polygon that has an area, but Shape_Area is 0 in the attribute table. Since it is very small anyway,
# I delete it before I execute the splitting.
# I also delete the 9 polygons with Shape_Area = 0.

# delete the polygon with UID = 822481 and with Shape_Area = 0 from featureClass, using the Update Cursor
in_feature = "featureClass"
fields = ["OBJECTID","Shape_Area"]

with arcpy.da.UpdateCursor(in_feature,fields) as cursor:
    for row in cursor:
        if row[0] = 822481:
            cursor.deleteRow()
        elif row[1] = 0:
                cursor.deleteRow()
            


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





