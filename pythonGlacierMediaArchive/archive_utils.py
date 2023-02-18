from datetime import datetime
import json
import os

import boto3
import database_utils
import scan_folders
import upload


def get_unarchived(category):
    folders = database_utils.get_not_uploaded(category)

    f = open('unarchived_folders_for_' + category + '.txt', 'w+', encoding="utf-8")
    for folder in folders:
        f.write(folder[0] + '\n')
    f.close()


def get_modified(category):
    scan_folders.scan_folders(category)
    all_archives = database_utils.get_all_uploaded(category)
    modified = []
    for archive in all_archives:
        if archive.DATE_ARCHIVED > archive.DATE_FOLDER_MODIFIED:
            modified.append(archive)
            print(archive)
    modified.append(archive)


def upsert_files(paths_file):
    f = open(paths_file, "r")
    paths = f.read().split('\n')
    for path in paths:
        if path:
            db_archive = database_utils.get_record(path)[0]
            print(db_archive)
            archive_id = ''
            if db_archive[5] :
                print('delete ' + db_archive[1])
                #delete_from_vault(db_archive[5])
            print(db_archive[0].split('\\')[-1].lower())
            if db_archive[2] == 'tv_shows' and 'season' not in db_archive[0].split('\\')[-1].lower():
                directory_list = os.listdir(db_archive[0])
                filtered_directory_list_paths = []
                for item in directory_list:
                    compound_path = path + "//" + item
                    if os.path.isfile(compound_path) or item.lower()[:6] != 'season':
                        filtered_directory_list_paths.append(compound_path)
                print('uploading ' + str(filtered_directory_list_paths))
                archive_id = 'testId'## upload.upload_archive(
                    #vault_name=db_archive[2],
                    #file_name=filtered_directory_list_paths.append(compound_path),
                   # arc_desc=db_archive[1],
                  #  part_size_mb=64,
                 #   num_threads='4' ##
                #)
            else:
                print('uploading ' + db_archive[0])
                archive_id = 'testId' ##upload.upload_archive(
                    #vault_name=db_archive[2],
                    #file_name=db_archive[0],
                   # arc_desc=db_archive[1],
                  #  part_size_mb=64,
                 #   num_threads='4'
                #)
            timestamp = datetime.timestamp(datetime.now())
            database_utils.upsert_archive_with_upload(db_archive[1], db_archive[0], db_archive[2],
                                      db_archive[3], str(timestamp), archive_id)

def delete_from_vault(glacier_id, category):
    with open("./config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    glacier = boto3.client("glacier",
                           aws_access_key_id=config.aws_key,
                           aws_secret_access_key=config.aws_secret_key)
    glacier.delete_archive(
        vaultName=category,
        archiveId=glacier_id)
