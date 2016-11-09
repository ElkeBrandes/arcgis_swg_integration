# arcgis_swg_integration
ArcGIS workflow to identify subfield areas that should be converted to switchgrass, based on yield, patch size, and distance of small patches to larger patches.

This repo includes python scripts that run processes in ArcGIS.

I am starting the repo with the files that I have worked on to date.


The .cmd files are to run python scripts in the windows command line. I used them for scripts that require arguments to pass and are run multiple times with changing arguments.

SubfieldSwg01add_calculate_cluid_mukey_test.py:
This script did not work, I ended up doing the cluid_mukey calculation in ArcMap.

SubfieldSwg01delete_split.py:
Workaround script, see comments in script

SubfieldSwg01reproject_join.py:
This script includes steps to prepare the feature class and join yield data and yield cut-offs per county, so that the yield-based scenarios can be run with the next script.

SubfieldSwg02scenarios.py:
This script calculates for each subfield polygon if it falls into the category to be managed in switchgrass, each script run is one scenario with changing assumptions.
For each scenario, a new field (column) is written in the attribute table.
The scenarios include county-specific yield cut offs, based on historic corn and soybean yields.

SubfieldSwg03test_areas.py:
This script calculates the areas that would be managed in switchgrass for each scenario that is in the attribute table and exports it into a csv file.

SubfieldSwg04import_reproject_townships.py:
This script prepares the township shapefile for the overly of townships and subfield polygons.

!!Not tested yet!!
SubfieldSwg05spatial_join_townships.py:
This script assigns each subfield polygon to a township. If it overlaps with more than one township, the township is assigned that it is overlapping with the largest portion.
!!Not tested yet!!
