# create variables
area_field = "Shape_Area"
field = "in_swg_8_20000_20"
totalArea = 0
where_clause = '"scenario_field"' + " = 'TRUE'"
value = 0
resultsVector = []

# loop through the vector of column names to get a total ha value for each scenario
#for field in swgVector:
with arcpy.da.SearchCursor(featureClass, [area_field, field]) as cursor:
    for row in cursor:
        if row[1] == "TRUE":
            totalArea += row[0]
totalAreaHa = round(totalArea / 10000, 0)
print(totalAreaHa)
print("The total area under scenario " + str(field) + " is " + str(totalAreaHa) + " ha.")