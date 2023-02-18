import sqlite3


def database_setup():
    conn = sqlite3.connect('pythonGlacierMediaArchive.db')
    conn.execute('''
        CREATE TABLE ARCHIVES (
        PATH TEXT PRIMARY KEY, NAME TEXT, TYPE TEXT, DATE_FOLDER_MODIFIED TEXT, DATE_ARCHIVED TEXT, GLACIER_ID TEXT
        );
    ''')


def upsert_archive_with_scan(name, path, category, last_modified):
    conn = sqlite3.connect('pythonGlacierMediaArchive.db')
    name = name.replace('\'', '\'\'')
    path = path.replace('\'', '\'\'')

    upsert_query = '''
        INSERT INTO ARCHIVES (path, name, type, date_folder_modified) VALUES 
        ('{0}', '{1}', '{2}', '{3}') ON CONFLICT(path) 
        DO UPDATE SET date_folder_modified=excluded.date_folder_modified, 
        date_archived=excluded.date_archived, glacier_id=excluded.glacier_id;
    '''
    upsert_query_formated = upsert_query.format(path, name, category, last_modified)
    print(upsert_query_formated)
    conn.execute(upsert_query_formated)
    conn.commit()


def upsert_archive_with_upload(name, path, category, last_modified, archive_date, glacier_id):
    conn = sqlite3.connect('pythonGlacierMediaArchive.db')
    name = name.replace('\'', '\'\'')
    path = path.replace('\'', '\'\'')

    upsert_query = '''
        INSERT INTO ARCHIVES (path, name, type, date_folder_modified, date_archived, glacier_id) VALUES 
        ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}') ON CONFLICT(path) 
        DO UPDATE SET date_folder_modified=excluded.date_folder_modified, 
        date_archived=excluded.date_archived, glacier_id=excluded.glacier_id;
    '''
    upsert_query_formated = upsert_query.format(path, name, category, last_modified, archive_date, glacier_id)
    print(upsert_query_formated)
    conn.execute(upsert_query_formated)
    conn.commit()


def get_not_uploaded(category):
    conn = sqlite3.connect('pythonGlacierMediaArchive.db')
    cur = conn.cursor()

    select_query = '''
        select * from ARCHIVES WHERE GLACIER_ID IS NULL AND TYPE='{0}'
     '''
    select_query_formatted = select_query.format(category)

    cur.execute(select_query_formatted)

    return cur.fetchall()


def get_all_uploaded(category):
    conn = sqlite3.connect('pythonGlacierMediaArchive.db')
    cur = conn.cursor()

    select_query = '''
        select * from ARCHIVES WHERE GLACIER_ID IS NOT NULL AND TYPE='{0}'
     '''
    select_query_formatted = select_query.format(category)

    cur.execute(select_query_formatted)

    return cur.fetchall()


def get_record(path):
    conn = sqlite3.connect('pythonGlacierMediaArchive.db')
    cur = conn.cursor()
    path = path.replace('\'', '\'\'')

    select_query = '''
        select * from ARCHIVES WHERE PATH='{0}'
     '''
    select_query_formatted = select_query.format(path)
    print(select_query_formatted)

    cur.execute(select_query_formatted)

    return cur.fetchall()
