# this script is similar to SubfieldDNDC07_clip_features_county.py,
# except that I clip first and then join the economic values (delta NPV on target swg conversion areas)
# in this script, the feature class containing subfield areas (single polygons) is clipped to the
# delineation of a certain county. 

# note that I am working in with the same subfield feature class that I used to identify eligible
# switchgrass conversion areas.

# before clipping, I need to preserve the objectid because I need it later to join the attributes.
# since the clipped feature class features will be assigned a new objectid, starting from 1, I needed
# to create a new field and copy the old objectid as integer into that field that I called object_id.
# I did that in ArcMap.


print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# enter the fips of the county that should be selected
fips_select = "IA043"

# make a feature layer from the county selected from the county feature class
in_features = "Counties"
out_layer = str(fips_select) + "_layer"
where_clause = '"fips"' + " = '" + str(fips_select) + "'"
arcpy.MakeFeatureLayer_management(in_features, out_layer, where_clause)


print("Clipping subfield feature class to county feature class ...")
print("")

in_features = "SubfieldIA_single"
clip_features = out_layer
out_feature_class = "clumu_" + str(fips_select)
arcpy.Clip_analysis(in_features, clip_features, out_feature_class)

# list the fields and types of the clipped feature class

field_list = arcpy.ListFields(out_feature_class)

for field in field_list:
    print("{0} is of type {1}"
          .format(field.name, field.type))

# there are a lot of null values in the joined data, for those polygons that were not in
# corn and/or soybeans from 2012 to 2015. I can delete them before doing further
# calculations to avoid errors later on.

print("Deleting polygons with <Null> values ...")
print("")

feature_class = out_feature_class
value_field = "crop12"
where_clause = '"' + value_field + '" IS NULL'

with arcpy.da.UpdateCursor(feature_class, (value_field,), where_clause) as cursor:
    for row in cursor:
        cursor.deleteRow()
print("Finito!")
