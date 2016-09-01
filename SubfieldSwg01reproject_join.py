

# C:\\Python27\\ArcGISx6410.3\\python.exe C:\\Users\\ebrandes\\Documents\\swg_econ\\python\\SubfieldSwg01reproject_join.py

# enter parameters:
# (0) name of projected feature class (e.g. "SubfieldIA027")
# (1) table with yield data to be joined (e.g. "CornYields2011_2014.txt")

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"
import sys
print "Running against: {}".format(sys.version)

# set variables:
in_dataset = arcpy.GetParameterAsText(0)
field_name = "cluid_mukey"
field_type = "FLOAT"

# reproject the feature class to NAD 83 UTM Zone 15N
in_dataset = arcpy.GetParameterAsText(0)
out_dataset = str(in_dataset) + "_Projected"
out_coor_system = arcpy.SpatialReference('NAD 1983 UTM Zone 15N')
arcpy.Project_management(in_dataset, out_dataset, out_coor_system)

# check the spatial reference of the new feature class
featureClass = out_dataset
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print spatialRef.Name


# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name
    
# join with corn yield data
in_feature_class = featureClass
in_field = "cluid_mukey" 
join_table = arcpy.GetParameterAsText(1)
join_field = "cluid_mukey"
field_list = ["mean_corn_yield", "clumuha"]  # is "clumuha" needed?

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field_list)

# there are multipart polygons in the feature class that consist of one record (one cluid_mukey) but multiple polygons.
# Since we have to look at each polygon individually for its size and position in relation to others, we need to
# split all multipart polygons into singlepart polygons.
# The result is that there are duplicate records for some of the cluid_mukey records.
in_feature_class = featureClass
out_feature_class = str(in_dataset) + "_single"
arcpy.MultipartToSinglepart_management(in_feature_class, out_feature_class)





