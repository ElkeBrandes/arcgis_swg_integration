# arguments passed in the cmd script:
# sys.argv[1] the feature class that was amended by a field for each scenario
#   by running script SubfieldSwg02scenarios_IDLE.py (e.g. "SubfieldIA_single")


import csv # for export into csv file
import sys # for export into csv file
import arcpy
import re # regular expression, to extract the cutoff values out of the scenario names

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\DNDC\\switchgrass_integration.gdb"

# read through the table and calculate the total area that would be in switchgrass under a certain scenario


# Make a list of fields that start with "in_swg*"
featureClass = sys.argv[1]
swgList = arcpy.ListFields(featureClass, "in_swg*")
for field in swgList:
    print(field.name)

# make a vector of the field names in the list
swgVector = []
for field in swgList:
    swgVector.append(field.name)

print(swgVector)


# create variables
area_field = "Shape_Area"
fips_field = "fips"
totalArea = 0

# create a csv file to write the result into
f = open("C:\\Users\\ebrandes\\Documents\\swg_econ\\swg_areas\\swg_areas_results.csv", 'wb')
writer = csv.writer(f)
writer.writerow(('yield_scenario', 'yield_years' 'size_cutoff',\
                 'distance_cutoff', 'swg_area', 'swg_area_percent'))
######

# calculate total area in corn/soybean first to be able to calculate percentages below
totalCornSoy = 0
with arcpy.da.SearchCursor(featureClass, (fips_field, area_field,)) as cursor:
    for row in cursor:
        if row[0] is not None:
            totalCornSoy += row[1]
totalCornSoyHa = round(totalCornSoy / 10000, 0)
print("The total area in corn and soybean is " + str(totalCornSoyHa) + " ha.")

# loop through the vector of column names to get a total ha value for each scenario
for field in swgVector:
    totalArea = 0
    with arcpy.da.SearchCursor(featureClass, [area_field, field]) as cursor:
        for row in cursor:
            if row[1] == "TRUE":
                totalArea += row[0]
    totalAreaHa = round(totalArea / 10000, 0)
    print("The total area under scenario " + str(field) + " is " + str(totalAreaHa) + " ha.")
    values = re.findall(r'\d+', field) # create vector of numeric values in the field
    values = values[-3:] # get rid of the first '2' if exists
    values[:0] = [field[7:10]] # add 'min' or '2nd' to describe the scenario
    totalAreaPercent = round((totalAreaHa *100/totalCornSoyHa),1)
    writer.writerow((str(values[0]), str(values[1]), str(values[2]), str(values[3]), str(totalAreaHa), str(totalAreaPercent)))
f.close()

#####################



 
