# enter parameters:
# (0) the feature class that has been modified using the script "SubfieldSwg01reproject_join" (e.g. "SubfieldIA027_Projected")
# (1) yield cutoff, e.g. 8 (Mg/ha)
# (2) size cutoff, e.g. 5000 (m2) (meaning the size below a polygon is excluded from the area in switchgrass)
# (3) distance cutoff, e.g. 20 (m) (meaning the distance to a larger polygon that is tolerated to include a smaller polygon into the area)

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# check the spatial reference of the new feature class
featureClass = arcpy.GetParameterAsText(0)
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print spatialRef.Name

# select polygons with corn yield < a cut off yield (in Mg/ha)

in_feature = featureClass
out_layer = "SubfieldLowYield"
yield_cutoff = arcpy.GetParameter(1)
where_clause = '"mean_corn_yield field"' + " < " + str(yield_cutoff)
field = "mean_corn_yield"
arcpy.MakeFeatureLayer_management(in_feature, out_layer, where_clause) # creates a temporary layer in the memory. Might cause crashes with large data sets.

# dissolve polygons in feature layer, resulting in feature class 1
in_feature = "SubfieldLowYield"
out_feature_class = "featureClass1"
arcpy.Dissolve_management(in_feature, out_feature_class, "", "","SINGLE_PART", "DISSOLVE_LINES")

# delete the small polygons from featureClass1, using the Update Cursor
in_feature = "featureClass1"
field = "Shape_Area"
size_cutoff = arcpy.GetParameter(2)
print(size_cutoff)
with arcpy.da.UpdateCursor(in_feature,(field,)) as cursor:
    for row in cursor:
        if row[0] < size_cutoff:
            cursor.deleteRow()