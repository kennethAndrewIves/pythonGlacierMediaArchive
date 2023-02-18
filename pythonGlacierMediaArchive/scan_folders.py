import json
import os
import database_utils as database_utils


def scan_folders(category):
    paths = get_archives_by_category(category)
    for path in paths:
        path_array = path.split("\\")
        name = path_array[-1]
        if category == 'tv_shows':
            if name.lower()[:6] == 'season':
                name = path_array[-2] + " " + name
            else:
                name = name + " metadata"
        last_modified = os.path.getmtime(path)
        if category == 'tv_shows' and name[-8:] == 'metadata':
            directory_list = os.listdir(path)
            filtered_directory_list_paths = []
            for item in directory_list:
                compound_path = path + "//" + item
                if os.path.isfile(compound_path) or item.lower()[:6] != 'season':
                    filtered_directory_list_paths.append(compound_path)
            for item in filtered_directory_list_paths:
                current_m_time = os.path.getmtime(item)
                if current_m_time > last_modified:
                    last_modified = current_m_time
        database_utils.upsert_archive_with_scan(name, path, category, str(last_modified))
    print('done scaning!')


def get_archives_by_category(category):
    with open("./config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    actual_paths = [];
    for path in data["paths"]:
        if path["type"] == category:
            actual_paths.append(path["path"])

    archive_paths = [];
    for path in actual_paths:
        archive_paths.extend(get_archive_paths(path, category));
    return archive_paths


def get_archive_paths(path, category):
    path_array = path.split("\\")
    path_array.append('${finalWildCard}')
    archives_paths = []
    for path_element in path_array:
        if path_element[:2] == '${' and path_element[-1] == '}':
            new_paths = []
            for iterator, archives_path in enumerate(archives_paths):
                wildcard_directories = os.listdir(archives_path)
                for wildcard in wildcard_directories:
                    new_path = archives_path + "\\" + wildcard
                    if os.path.isdir(new_path):
                        new_paths.append(new_path)
            archives_paths = new_paths
        else:
            if archives_paths:
                for iterator, path in enumerate(archives_paths):
                    archives_paths[iterator] = (path + "\\" + path_element)
            else:
                archives_paths.append(path_element)
    if category == 'tv_shows':
        for path in archives_paths:
            season_folders = filter(lambda folder: folder.lower()[:6] == 'season', os.listdir(path))
            for folder in season_folders:
                new_path = path + "\\" + folder
                if os.path.isdir(new_path):
                    archives_paths.append(new_path)
    return archives_paths
