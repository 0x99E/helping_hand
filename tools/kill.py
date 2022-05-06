import os
cmd = "sudo fuser -k 333/tcp"
try:
    os.system(cmd)
except:
    print("Error: " + cmd)