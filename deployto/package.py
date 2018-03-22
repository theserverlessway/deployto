from io import BytesIO
import zipfile
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
                # print('{} {}'.format(source, target))
                zipfile_ob.write(source, target, zipfile.ZIP_DEFLATED)
            elif os.path.isdir(source):
                # print('{} {}'.format(source, target))
                for root, dirs, files in os.walk(source):
                    target_folder = root.replace(source, '', 1) or '/'
                    for file in files:
                        target_file = target + target_folder + '/' + file
                        zipfile_ob.write(os.path.join(root, file), target_file, zipfile.ZIP_DEFLATED)
    return file_like_object.getvalue()
