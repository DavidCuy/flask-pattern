import os
from typing import List
from ...config.storage import config

class LocalStorage:
    def __init__(self) -> None:
        self.initial_path = config['local']['initial_path']
        if not os.path.exists(self.initial_path):
            try:
                os.makedirs(self.initial_path)
            except OSError:
                print (f"Creation of the directory {self.initial_path} failed")
            else:
                print (f"Successfully created the directory {self.initial_path}")
            

    def list_files(self, path: str = "") -> List[str]:
        source_folder = os.path.join(self.initial_path, path)
        files = os.listdir(source_folder)
        return list(filter(lambda f: not str(f).startswith('.'), files))
    
    def get(self, path: str) -> bytes:
        path = os.path.join(self.initial_path, path)
        try:
            with open(path, 'rb') as f:
                content = f.read()
                f.close()
        except (FileNotFoundError, IOError) as e:
            #traceback.print_exc(file=sys.stdout)
            #print(str(e))
            raise(e)
        return content
    
    def put(self, path: str, content: bytes) -> bool:
        path = os.path.join(self.initial_path, path)
        try:
            with open(path, 'wb') as f:
                f.write(content)
                f.close()
        except (FileNotFoundError, IOError) as e:
            #print(str(e))
            raise(e)
        return True
    
    def delete(self, path: str) ->  bool:
        file_path = os.path.join(self.initial_path, path)
        os.remove(file_path)
        return not os.path.exists(file_path)