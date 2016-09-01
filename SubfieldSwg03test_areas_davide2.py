import csv
import sys

# read through the table and calculate the total area that would be in switchgrass under a certain scenario

# read the fields in a feature class
#fieldList = arcpy.ListFields(featureClass)
# loop through each field in the list and print the name
#for field in fieldList:
#    print field.name

# Make a list of fields that start with "in_swg*"
swgList = arcpy.ListFields(featureClass, "in_swg*")
#test print
#for field in swgList:
#    print(field.name)


swgVector = []
for field in swgList:
    swgVector.append(field.name)
#test print
#print(swgVector)


# create variables
area_field = "Shape_Area"
totalArea = 0
where_clause = '"scenario_field"' + " = 'TRUE'"
value = 0
resultsVector = []

# loop through the vector of column names to get a total ha value for each scenario
for field in swgVector:
    totalArea = 0
    with arcpy.da.SearchCursor(featureClass, [area_field, field]) as cursor:
        for row in cursor:
            if row[1] == "TRUE":
                totalArea += row[0]
    totalAreaHa = round(totalArea / 10000, 0)
    print("The total area under scenario " + str(field) + " is " + str(totalAreaHa) + " ha.")


#f = open('MusineCSV.csv', 'wb')
#writer = csv.writer(f)
#writer.writerow( ('Musine scenario', 'Musine Area'))
#for field in swgVector:
#    totalArea = 0
#    with arcpy.da.SearchCursor(featureClass, [area_field, field]) as cursor:
#        for row in cursor:
#            if row[1] == "TRUE":
#                totalArea += row[0]
#    totalAreaHa = round(totalArea / 10000, 0)
#    writer.writerow((str(field), str(totalAreaHa)))
#f.close()

# tried to write the data into a csv file but couldn't figure it out:
    
#    value = (field, totalAreaHa)
#    resultsVector.append(value)
#    with open('swg_output', 'w') as csvfile:
#        writer = csv.writer(csvfile)
#        [writer.writerow(r) for r in resultsVector]

#with open('swg_output', 'r') as csvfile:
#    reader = csv.reader(csvfile)
#    table = [[str(e) for e in r]for r in reader]
    


 