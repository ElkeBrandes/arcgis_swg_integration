# enter parameters:
# (0) name of projected feature class (e.g. "SubfieldIA027")
# (1) table with yield data to be joined (e.g. "CornYields2011_2014.txt")

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# set variables:
in_dataset = arcpy.GetParameterAsText(0)
field_name = "cluid_mukey"
field_type = "DOUBLE"

# delete field
arcpy.DeleteField_management(in_dataset, field_name)

# create a field with cluid_mukey in the feature class
arcpy.AddField_management(in_dataset, field_name, field_type)

# calculate the field with the update cursor
with arcpy.da.UpdateCursor(in_dataset, (field_name,)) as cursor:
    for row in cursor:
        row[0] = float(str("cluid") + "mukey")
