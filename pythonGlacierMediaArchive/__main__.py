import scan_folders
import database_utils
import archive_utils
import sys

if __name__ == "__main__":
    if sys.argv[1] == 'dbcreate':
        database_utils.database_setup()
    if sys.argv[1] == 'scan_folders':
        scan_folders.scan_folders(sys.argv[2])
    if sys.argv[1] == 'upload_folders':
        # arg 2 must be a file
        archive_utils.upsert_files(sys.argv[2])
    if sys.argv[1] == 'generate_unarchived':
        archive_utils.get_unarchived(sys.argv[2])
    if sys.argv[1] == 'generate_modified':
        archive_utils.get_modified(sys.argv[2])
