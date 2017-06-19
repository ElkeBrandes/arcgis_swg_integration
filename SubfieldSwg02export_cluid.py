Input_Feature_Class = "SubfieldIA_single"
Value_Field = ["OBJECTID", "cluid", "Shape_Area"]
Delimiter = "SPACE"
Output_ASCII_File = "C:\\Users\\ebrandes\\Documents\\swg_econ\\tables\\swg_econ_cluid.txt"


arcpy.ExportXYv_stats(Input_Feature_Class, Value_Field, Delimiter, Output_ASCII_File, "ADD_FIELD_NAMES")
