import litepkg
import logging
import requests
import hashlib
import os
import config
import shutil

def validate_local_name(local_name):
    if '/' in local_name or '\\' in local_name:
        logging.error("Local path name '{}'".format(local_name) +
        " contains illegal characters, aborting")
        exit(1)

def download_file(url, local_name, sha1=None, md5=None):
    """download_file

    :param url: URL to download from
    :param local_name: name within working directory
    :param sha1: SHA1 hexdigest, None to ignore
    :param md5: md5 hexdigest, None to ignore
    """
    validate_local_name(local_name)
    logging.debug("Downloading '{}' to '{}'".format(url, local_name))
    logging.info("Downloading file '{}'...".format(url))
    r = requests.get(url, allow_redirects=True)
    with open(os.path.join("./", local_name), 'wb') as f:
        f.write(r.content)

    if not os.path.exists(local_name):
        logging.error("Downloading file '{}' failed.".format(local_file))
        exit(1)

    if sha1 is not None:
        file_sha1 = hashlib.sha1(open(local_name, 'rb').read()).hexdigest()
        if file_sha1 != sha1:
            logging.error("Incorrect shasum for '{}'. Got '{} but."
                          .format(local_name, file_sha1) +
                          "expected '{}'.".format(sha1))

    if md5 is not None:
        file_md5 = hashlib.md5(open(local_name, 'rb').read()).hexdigest()
        if file_md5 != md5:
            logging.error("Incorrect shasum for '{}'. Got '{} but."
                          .format(local_name, file_md5) +
                          "expected '{}'.".format(md5))

    logging.info("Download finished successfully.")


def get_artifact_directory(package_name):
    return os.path.join(config.args.artifacts_directory, package_name)

def set_artifact(package_name, local_name):
    litepkg.ensure_dir_exists(get_artifact_directory(package_name))

    if os.path.isfile(local_name):
        logging.info("Copying file '{}'".format(local_name))
        dst_file = os.path.join(get_artifact_directory(package_name),
                                local_name)
        shutil.copyfile(local_name, dst_file)
        logging.info("Finished copying file.")
    elif os.path.isdir(local_name):
        logging.info("Copying directory '{}'".format(local_name))
        shutil.copytree(local_name, get_artifact_directory(package_name))
    else:
        logging.info("'{}': not a file or directory, don't know what to do"
                     .format(local_name))








def test_func():
    logging.info("In test_func")
