
import arcpy
from arcpy import env
from arcpy.sa import *

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# split multipart polygons to single polygons in the feature class "Test_SubfieldIA181_Selection"

in_feature_class = "Test_SubfieldIA181_Selection"
out_feature_class = "test_subfield_single"
arcpy.MultipartToSinglepart_management(in_feature_class, out_feature_class)

# make raster layers from the feature classes "test_subfield_single" and "Test_Townships"

in_features = out_feature_class
value_field = "OBJECTID"
out_rasterdataset_1 = "test_subfield_raster"
arcpy.PolygonToRaster_conversion(in_features, value_field, \
                                 out_rasterdataset_1, "MAXIMUM_COMBINED_AREA", "", 30)
# the OBJECTID from the feature layer turns into the field "value" in the raster. Because not every feature is
# converted into a raster class because some are too small, the number of OBJECTID in the raster is smaller than
# the number of OBJECTID in the feature class.

# environment setting: snap raster
raster = "test_subfield_raster"
arcpy.env.snapRaster = raster

in_features = "Test_Townships"
value_field = "politwp_id"
out_rasterdataset_2 = "test_twp_raster"
arcpy.PolygonToRaster_conversion(in_features, value_field, \
                                 out_rasterdataset_2, "MAXIMUM_COMBINED_AREA", "", 30)


# run zonal statistics on the data, using "test_subfield_raster" as the zone raster and
# "test_twp_raster" as the evaluated raster

in_zone_data = out_rasterdataset_1
zone_field = "value"
in_value_raster = out_rasterdataset_2
out_table = "test_twp_majority"
arcpy.ZonalStatisticsAsTable(in_zone_data, zone_field, in_value_raster, out_table, "MAJORITY")



# make a feature layer from the feature classes "Test_SubfieldIA181_Selection" and "Test_Townships"

#arcpy.MakeFeatureLayer_management("Test_SubfieldIA181_Selection", "test_subfield")
#arcpy.MakeFeatureLayer_management("Test_Townships", "test_twp")

# select the features that cross township borders
#in_layer = "test_subfield"
#overlap_type = "CROSSED_BY_THE_OUTLINE_OF"
#select_features = "test_twp"
#arcpy.SelectLayerByLocation_management(in_layer, overlap_type, select_features)


# Open a search cursor on the test_subfield layer (only applies to selected features)
#with arcpy.da.SearchCursor(in_layer, ("cluid_mukey",)) as cursor:
#        for row in cursor:
#            print int(row[0])
#            if 


# for each row:
# - create a new field "twpid"
# - enter the twpid of the twp that the polygon overlaps with the largest area

# solutions:(?)
# do an intersect of twp and subfield layers: subfield_twp_intersect
