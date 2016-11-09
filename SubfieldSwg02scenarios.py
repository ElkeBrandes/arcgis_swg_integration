# arguments passed with the cmd script:
# sys.argv[1] the feature class that has been modified using the script
#   "SubfieldSwg01reproject_join" (e.g. "SubfieldIA_single")

# sys.argv[2] corn yield cutoff: a field in the feature class that has been joined in the preceding script.
#   E.g., "cut_cg_min_16" means the cut off for corn which is the minimum yield per county between 2000 and 2015.

# sys.argv[3] soybean yield cutoff: a field in the feature class that has been joined in the preceding script.
#   E.g., "cut_sb_min_16" means the cut off for soybean which is the minimum yield per county between 2000 and 2015.

# sys.argv[4] size cutoff, e.g. 5000 (m2) (meaning the size below a
#   polygon is excluded from the area in switchgrass)

# sys.argv[5] distance cutoff, e.g. 20 (m) (meaning the distance to a
#   larger polygon that is tolerated to include a smaller polygon into the area)

print("Running script ...")

import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = r"C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# check the spatial reference of the new feature class
featureClass = sys.argv[1]
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print("Just checking ... Reference System is " + str(spatialRef.Name) + ".") # not really needed, just for checking

# select polygons with corn and soybean yields < a county-specific cut off yield (in Mg/ha)
# we are looking at a cutoff that refers to each yield in each year, 2011-2014
# not the mean yields!

# loop through the attribute table to select features that fall under the cut off values
cg_cutoff_field = sys.argv[2]
sb_cutoff_field = sys.argv[3]

with arcpy.da.SearchCursor(featureClass, (cg_cutoff_field, sb_cutoff_field)) as cursor:
    for row in cursor:
        where_clause = '(("crop12" = ' + " 'CG' AND " + '"yield12" < "' + \
               cg_cutoff_field + '") OR ("crop12"' + " = 'SB' AND " + '"yield12" < "' + \
               sb_cutoff_field + '")) AND (("crop13"' + " = 'CG' AND " + '"yield13" < "' + \
                cg_cutoff_field + '") OR ("crop13"' + " = 'SB' AND " + '"yield13" < "' + \
                sb_cutoff_field + '")) AND (("crop14"' + " = 'CG' AND " + '"yield14" < "' + \
                cg_cutoff_field + '") OR ("crop14"' + " = 'SB' AND " + '"yield14" < "' + \
                sb_cutoff_field + '")) AND (("crop15"' + " = 'CG' AND " + '"yield15" < "' + \
                cg_cutoff_field + '") OR ("crop15"' + " = 'SB' AND " + '"yield15" < "' + \
                sb_cutoff_field + '"))'
        arcpy.selectLayerByAttribute_management(featureClass, "ADD_TO_SELECTION", where_clause)

# dissolve polygons in feature layer, resulting in feature class 1
in_feature = featureClass
out_feature_class = "featureClass1"
arcpy.Dissolve_management(in_feature, out_feature_class, "", "","SINGLE_PART", "DISSOLVE_LINES")

# clean up in memory layer
arcpy.Delete_management("SubfieldLowYield")

# from featureClass1, select by attribute polygons < a cut off size (in square meters)
in_feature = "featureClass1"
out_layer = "SubfieldLowYieldSmall"
size_cutoff = sys.argv[4]
where_clause = '"Shape_Area" < ' + str(size_cutoff)
arcpy.MakeFeatureLayer_management(in_feature, out_layer, where_clause)

# create featureClass2 from feature layer (only the small polygons)
in_feature = "SubfieldLowYieldSmall"
out_feature = "featureClass2"
arcpy.CopyFeatures_management(in_feature, out_feature)

# delete the small polygons from featureClass1, using the Update Cursor
in_feature = "featureClass1"
field = "Shape_Area"

with arcpy.da.UpdateCursor(in_feature,(field,)) as cursor:
    for row in cursor:
        if row[0] < float(size_cutoff):
            cursor.deleteRow()

# from featureClass2: select by location polygons within a defined distance (in meters) of a larger polygon
# make two layers first, one from featureClass1 and one from featureClass2:
arcpy.MakeFeatureLayer_management("featureClass2", "SubfieldLowYieldSmall")
arcpy.MakeFeatureLayer_management("featureClass1", "SubfieldLowYieldLarge")

in_layer = "SubfieldLowYieldSmall"
overlap_type = 'WITHIN_A_DISTANCE'
select_layer = "SubfieldLowYieldLarge"
distance_cutoff = sys.argv[5]
search_distance = int(distance_cutoff)

arcpy.SelectLayerByLocation_management(in_layer, overlap_type, select_layer, search_distance)

# clean up in memory layer
arcpy.Delete_management("SubfieldLowYieldLarge")

# create feature class 3 from feature layer (only small polygons close to larger ones)
in_feature = "SubfieldLowYieldSmall"
out_feature = "featureClass3"
arcpy.CopyFeatures_management(in_feature, out_feature)

# clean up in memory layer
arcpy.Delete_management("SubfieldLowYieldSmall")

# merge featureClass1 and featureClass3 to get featureClass4
inputs = ["featureClass1", "featureClass3"]
output = "featureClass4"
arcpy.Merge_management(inputs, output)

# add an attribute field to featureClass
in_feature = featureClass
field_name = "in_swg" + "_" + str(corn_yield_cutoff) + "_" + str(soy_yield_cutoff) + "_" + str(
    size_cutoff) + "_" + str(distance_cutoff) 
field_type = "TEXT"
arcpy.AddField_management(in_feature, field_name, field_type)
print("Added new field to " + str(sys.argv[1]) + ": " + str(field_name) + ".")

# using update cursor to go through the rows of SubfieldIA_single and check for two spatial attributes,
# enter "TRUE" into column "in_swgX" if feature should be in switchgrass
print("Going through features looking for those that fit into the scenario...")
# make feature layer from featureClass
in_feature = featureClass
out_layer = "allSubfield"
overlap_type1 = "WITHIN_CLEMENTINI"
overlap_type2 = "CONTAINS"
select_features = "featureClass4"
arcpy.MakeFeatureLayer_management(in_feature, out_layer)
arcpy.SelectLayerByLocation_management(out_layer, overlap_type1, select_features)
arcpy.SelectLayerByLocation_management(out_layer, overlap_type2, select_features, 0 ,"ADD_TO_SELECTION")
count = 0
with arcpy.da.UpdateCursor(out_layer, (field_name,)) as cursor:
    for row in cursor:
        row[0] = "TRUE"  #adds "TRUE" to all the selected features
        cursor.updateRow(row)
        count += 1       # counts all selecetd features
print("Done. Counted "  + str(count) + " features in " + str(sys.argv[1]) +" that fall into the category.")
print("Deleting interim feature classes ...")

# clean up in memory layer
arcpy.Delete_management("allSubfield")

# clean up interim feature classes
arcpy.Delete_management("featureClass1")
arcpy.Delete_management("featureClass2")
arcpy.Delete_management("featureClass3")
arcpy.Delete_management("featureClass4")

print("Done. Yay!")

