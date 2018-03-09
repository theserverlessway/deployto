from io import BytesIO
import zipfile
import glob
import os


def package(paths):
    file_like_object = BytesIO()
    with zipfile.ZipFile(file_like_object, 'w') as zipfile_ob:
        for path in paths:
            split = path.split(':', 1)
            source = split[0]
            target = source

            if len(split) == 2:
                target = split[1]
            if os.path.isfile(source):
                if not target:
                    target = os.path.basename(source)
                zipfile_ob.write(source, target, zipfile.ZIP_DEFLATED)
            elif os.path.isdir(source):
                for name in glob.glob("{}/*".format(source)):
                    target_file = target + '/' + os.path.basename(name)
                    zipfile_ob.write(name, target_file, zipfile.ZIP_DEFLATED)
    return file_like_object.getvalue()
