from io import BytesIO
import zipfile
import glob
import os


def package(paths):
    file_like_object = BytesIO()
    with zipfile.ZipFile(file_like_object, 'w') as zipfile_ob:
        for path in paths:
            prefix = path
            split = path.split(':', 1)
            if len(split) == 2:
                prefix = split[1]
            for name in glob.glob("{}/*".format(split[0])):
                target = prefix + '/' + os.path.basename(name)
                zipfile_ob.write(name, target, zipfile.ZIP_DEFLATED)
    return file_like_object.getvalue()
