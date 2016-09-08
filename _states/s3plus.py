# State module for s3plus


# Import python libs
from __future__ import absolute_import

try:
    from boto.s3.connection import S3Connection as s3
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

# Define the module's virtual name
__virtualname__ = 's3plus'


def __virtual__():
    if not HAS_BOTO:
        return False
    return __virtualname__


def exists(name, bucket, files, path):

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}

    changes = []

    __salt__['file.mkdir'](dir_path=path)

    if type(files) is list:
        for file in files:
            filepath = '{0}/{1}'.format(path, file)
            if __salt__['file.file_exists'](filepath):
                changes.append('{0} already exists.'.format(file))
            else:
                __salt__['s3plus.get_file'](
                    objectid=file,
                    bucketname=bucket,
                    path='{0}/{1}'.format(path, file))
                changes.append('{0} was downloaded'.format(file))

    elif type(files) is str:
        #check if file exists
        filepath = '{0}/{1}'.format(path, files)
        if __salt__['file.file_exists'](filepath):
            changes.append('{0} already exists.'.format(files))
        else:
            __salt__['s3plus.get_file'](
                objectid=file,
                bucketname=bucket,
                path='{0}/{1}'.format(path, file))
            changes.append('{0} was downloaded'.format(files))

    else:
        ret['result'] = False
        ret['comment'] = 'Files must be string or list'

    ret['changes'] = changes
    return ret
