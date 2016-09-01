import sys
print "Running script against: {}".format(sys.version)

# enter parameters:
arg1 =  "SubfieldIA_Projected"

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "E:\\switchgrass_integration.gdb"

###############################################################################################################################
#
#  # MultipartToSinglepart does not work: ExecuteError: ERROR 000072: Cannot process feature with OID 822481
#  # This is a strange polygon that has an area, but Shape_Area is 0 in the attribute table. Since it is very small anyway,
#  # I delete it before I execute the splitting.
#  # I also delete the 9 polygons with Shape_Area = 0.
#  
#  # delete the polygon with UID = 822481 and with Shape_Area = 0 from featureClass, using the Update Cursor
in_feature = arg1
fields = ["OBJECTID","Shape_Area"]

with arcpy.da.UpdateCursor(in_feature,fields) as cursor:
   for row in cursor:
       if row[0] == 822481:
           cursor.deleteRow()
       elif row[0] == 2929121:
           cursor.deleteRow()  
       elif row[1] == 0:
           cursor.deleteRow()

###############################################################################################################################
            


print("Splitting multipart features ...")
# there are multipart polygons in the feature class that consist of one record (one cluid_mukey) but multiple polygons.
# Since we have to look at each polygon individually for its size and position in relation to others, we need to
# split all multipart polygons into singlepart polygons.
# The result is that there are duplicate records for some of the cluid_mukey records.
in_feature_class = arg1
out_feature_class = "SubfieldIA" + "_single"
arcpy.MultipartToSinglepart_management(in_feature_class, out_feature_class)
print("")
print("Done. Yippie!")





