import subprocess
cmd = 'C:\\Users\\ebrandes\\Documents\\swg_econ\\pythonSubfieldSwg02scenarios.py'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell = True)
out, err = p.communicate() 
result = out.split('\n')
for lin in result:
    if not lin.startswith('#'):
        print(lin)