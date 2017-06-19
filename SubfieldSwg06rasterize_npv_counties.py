# this script I rasterize the three selected counties:
# Harrison (IA085), Poweshiek (IA157), and Clayton (IA043)


print("Running script ...")
print("")
import arcpy
import sys
from arcpy.sa import *  #spatial analyst extension
from arcpy import env

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"


# create a feature layer from the input feature class 
print("")
print("Creating a feature layer...")
in_features = "clumu_IA043"
out_layer = str(in_features) + "_layer"
arcpy.MakeFeatureLayer_management(in_features, out_layer)


# convert the feature layer to a raster containing the delta NPV data.
print("")
print("Creating raster 1...")
value_field = "d_npv"
out_raster = "clumu_IA043_raster"
cellsize = 10
arcpy.PolygonToRaster_conversion(out_layer, value_field, out_raster, cellsize = cellsize)

# convert the feature layer to a raster containing the fips data.
print("")
print("Creating raster 2...")
value_field = "fips"
out_raster = "clumu_IA043_raster_all"
cellsize = 10
arcpy.PolygonToRaster_conversion(out_layer, value_field, out_raster, cellsize = cellsize)

# clean up in memory layer
arcpy.Delete_management(out_layer)

print("")
print("Done. Yippie!")

