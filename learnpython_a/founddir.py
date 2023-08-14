import os
dir = "C:\\Users\\zhnl2\\Documents\\dev\\projects"
for root, dirs, files in os.walk(dir):
  for file in files:
    print(os.path.join(root,file))