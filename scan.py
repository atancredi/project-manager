import os
from json import loads, dumps
from dotenv import load_dotenv

# get files to scan inside subfolders
def get_files_to_scan(path, ignore_folders = None):
    # get files to scan
    files_to_scan = []
    
    path = os.path.abspath(path)
    for _file in os.listdir(path):
        _file = path+"/"+_file
        if os.path.isdir(_file):
            if ignore_folders is not None and _file.split("/")[-1] in ignore_folders:
                print("Ignoring folder: "+_file)
                continue
            files_to_scan += get_files_to_scan(_file, ignore_folders)
        if os.path.isfile(_file) and \
            _file[0] != '.' \
            and _file.split('.')[-1].lower() == 'py':
                files_to_scan.append(os.path.abspath(_file))

    return files_to_scan

# scan for todos inside files designated
def scan_folder(path):
    
    ignore_folders = loads(os.environ.get('IGNORE_FOLDERS'))
    files_to_scan = get_files_to_scan(path, ignore_folders)

    # scan each file for TODOs
    todos = []
    for file in files_to_scan:
        cnt = 1
        with open(os.path.abspath(file),"r") as f:
            for line in f:
                line = line.strip()
                if "TODO " in line and line[0] == "#":
                    assignment = "".join(line.split("TODO")[1]).strip()
                    todos.append({
                        "file": os.path.abspath(file),
                        "todo": assignment,
                        "line": cnt
                    })
                cnt += 1
    return todos
    
def write_report(todos, path=None):
    if path is None:
        path = "report.json"

    if not os.path.exists(path):
        raise FileNotFoundError("Report file not found: "+path)

    if os.path.isdir(path):
        path = path+'/report.json'

    with open(path,"w") as f:
        f.write(dumps(todos,indent=4))

if __name__ == '__main__':
    load_dotenv()
    res = scan_folder('/media/aletanc/Arfietto/Users/aless/source/AIT')
    
    # write_report(res,'/home/aletanc/ale-vault/Projects')
    