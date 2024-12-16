

import os
from django.core.files.storage import FileSystemStorage

class NoLockingFileSystemStorage(FileSystemStorage):
    def _save(self, name, content):
        # Bypass locking mechanism
        full_path = self.path(name)
        directory = os.path.dirname(full_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write content to file without locking
        with open(full_path, 'wb') as f:
            for chunk in content.chunks():
                f.write(chunk)
        return name
