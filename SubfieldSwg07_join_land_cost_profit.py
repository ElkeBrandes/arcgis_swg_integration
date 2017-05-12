

import sys
print "Running script against: {}".format(sys.version)

# the arguments noted below as sys.argv[1] and sys.argv[2] are passed in the cmd script "SubfieldSwg.cmd".
# They refer to the two files, the Iowa subfield feature class and the txt file containing the
# attributes (yield and yield cut off data)

import arcpy
# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"


featureClass = "ia_clumu_2016_single"

# read the fields in a feature class
fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
for field in fieldList:
    print field.name

print("Importing txt file into geodatabase ...")

# yield and cut off data (table)
in_rows ="C:\\Users\\ebrandes\\Documents\\swg_econ\\tables\\clumu_cgsb_profit_land_values_mean_2012_2015.txt"
out_path = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"
out_name = "land_cost_profit_2012_2015"
arcpy.TableToTable_conversion(in_rows, out_path, out_name)
    
print("Joining with 2012-2015 mean profit data calculated using land costs ...")

# join with corn yield data
in_feature_class = featureClass
in_field = "cluid_mukey" 
join_table = out_name
join_field = "cluid_mukey"
field = "profit_land_cost_ha" 

arcpy.JoinField_management(in_feature_class, in_field, join_table, join_field, field)


print("")
print("Done. Yippie!")





