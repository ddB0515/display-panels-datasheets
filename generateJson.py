import os 
import json 
from pathlib import Path 
from filecmp import cmp

# Specify the path to the folder you want to create the JSON for 
folder_path = 'datasheets'
totalFiles = 0
totalChildFiles = 0

def generate_folder_json(path): 
    global totalFiles
    global totalChildFiles
    # Initialize the result dictionary with folder 
    # name, type, and an empty list for children 
    result = {'name': os.path.basename(path), "totalFiles": totalChildFiles,
              'type': 'folder', 'children': []} 

    # Check if the path is a directory 
    if not os.path.isdir(path): 
        return result 
  
    # Iterate over the entries in the directory 
    sortedDir = os.listdir(path)
    sortedDir.sort()
    for entry in sortedDir: 
       # Create the full path for the current entry 
        entry_path = os.path.join(path, entry) 
  
        # If the entry is a directory, recursively call the function 
        if os.path.isdir(entry_path): 
            result['children'].append(generate_folder_json(entry_path)) 
        # If the entry is a file, create a dictionary with name and type 
        else: 
            result['children'].append({'name': entry.rstrip(), 'type': 'file'}) 
            totalChildFiles = totalChildFiles + 1
    
    result['totalFiles'] = totalChildFiles
    totalFiles = totalFiles + totalChildFiles
    totalChildFiles = 0
    return result 
  

DATA_DIR = Path(folder_path) 
files = sorted(os.listdir(folder_path)) 

# List having the classes of documents 
# with the same content 
duplicateFiles = [] 
  
# comparison of the documents 
for file_x in files: 
  
    if_dupl = False
  
    for class_ in duplicateFiles: 
        # Comparing files having same content using cmp() 
        # class_[0] represents a class having same content 
        if_dupl = cmp( 
            DATA_DIR / file_x, 
            DATA_DIR / class_[0], 
            shallow=False
        ) 
        if if_dupl: 
            class_.append(file_x) 
            break
  
    if not if_dupl: 
        duplicateFiles.append([file_x]) 
# Print results 
print(duplicateFiles) 

# Call the function to create the JSON from folder 
folder_json = generate_folder_json(folder_path) 
# Add total files at the end
folder_json["totalFiles"] = totalFiles
  
# Save to a JSON file with indentation 
with open('datasheets.json', 'w', encoding='utf-8') as f:
    json.dump(folder_json, f, ensure_ascii=False, indent=4)
