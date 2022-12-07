import pyodbc
import csv
import importlib

IDS = "206202384_204864532"
################################################
SERVER_NAME = "techniondbcourse01.database.windows.net"
DATABASE_NAME = "shai0k"
USER_NAME = "shai0k"
PASSWORD = "Qwerty12!"
################################################
NUMBER_OF_TESTS = 1
FILES_PATH = "./data/"
queries_file = importlib.import_module(IDS)
queries_answer = queries_file.QUERIES_ANSWER

"""
IMPORTANT NOTES: We assume that the following files exist in the path specified in FILES_PATH:
* SQL file, named as "create_table_commands_PartB.sql", with the create tables commands.
* CSV files containing the data to be uploaded to the database. 
The name of each file is "<table_name>_test<test_num>.csv" where <table_name> and <test_num> are the table name and
test number, respectively. 
* CSV files containing the correct result for each query. 
The name of each file is "correct_result_q<q_number>_test<test_num>.csv" where and <test_num> are the query number and
test number, respectively.
"""
################################################
# DO NOT CHANGE THE INFORMATION BELOW!
CREATE_TABLES_FILE_NAME = FILES_PATH + "create_table_commands_PartB.sql"
TABLES = ['Employee', 'Project', 'WorkOnProject']
QUERIES_RESULT_TYPE = {2: 'set', 3: 'list', 4: 'set'}
# We use list for queries with ORDER BY. We assume that there are no duplicates
QUERY_NUMBERS = [2, 3, 4]
################################################


def db_connect(server_name, database, user, pwd):
    cnxn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=' + server_name + ';'
                          'DATABASE=' + database + ';'
                          'UID=' + user + ';'
                          'PWD=' + pwd + '')
    cursor = cnxn.cursor()
    return cnxn, cursor


def create_tables(cursor):
    for table_name in TABLES[::-1]:
        drop_sql = "DROP TABLE IF EXISTS " + table_name
        cursor.execute(drop_sql)
        cursor.commit()
    create_tables_file = open(CREATE_TABLES_FILE_NAME, 'r')
    create_tables_commands = create_tables_file.read()
    create_tables_file.close()
    sqlCommands = create_tables_commands.split(';')
    for command in sqlCommands[:-1]:
        try:
            cursor.execute(command)
            cursor.commit()
        except:
            print("Command skipped: ", command)


def insert_data_to_tables(cursor, file_path, table_name):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        columns = next(reader)
        data_to_upload = []
        for data in reader:
            data_to_upload.append('(' + ','.join([f"'{item}'" for item in data]) + ')')
            if len(data_to_upload) >= 1000:
                query = f"insert into {table_name}({','.join(columns)}) values "
                query += ','.join(data_to_upload)
                cursor.execute(query)
                cursor.commit()
                data_to_upload = []
        query = f"insert into {table_name}({','.join(columns)}) values "
        query += ','.join(data_to_upload)
        cursor.execute(query)
        cursor.commit()


def get_correct_result_from_file(file_path, q_number, query_result_type, test_number):
    with open(f'{file_path}correct_result_q{q_number}_test{test_number}.csv', 'r') as f:
        reader = csv.reader(f)
        columns = next(reader)
        correct_result = [tuple([str(elem) for elem in row]) for row in reader]
        if query_result_type == 'set':
            correct_result = set(correct_result)
        return correct_result


def get_query_result(cursor, query, q_number, query_result_type):
    try:
        cursor.execute(query)
        query_result = [tuple([str(elem) for elem in data]) for data in cursor.fetchall()]
        if query_result_type == 'set':
            query_result = set(query_result)
        return query_result
    except Exception as e:
        print(f"Error occurred when executing q_{q_number}")
        print(e)
        return "ERROR"


if __name__ == "__main__":
    cnxn, cursor = db_connect(SERVER_NAME, DATABASE_NAME, USER_NAME, PASSWORD)
    create_tables(cursor)
    for test_num in range(1, NUMBER_OF_TESTS + 1):
        print(f"Test number {test_num}")

        # Uploading the data to the tables
        for table_name in TABLES:
            insert_data_to_tables(cursor, f'{FILES_PATH}{table_name}_test{test_num}.csv', table_name)

        for q_number in QUERY_NUMBERS:
            query_result_type = QUERIES_RESULT_TYPE[q_number]
            correct_result = get_correct_result_from_file(FILES_PATH, q_number, query_result_type, test_num)
            sql_commands = queries_answer[f"Q{q_number}"]
            students_query_result = get_query_result(cursor, sql_commands, q_number, query_result_type)
            if correct_result == students_query_result:
                print(f"Correct result for query {q_number}")
            else:
                print(f"Incorrect result for query {q_number}")

        # Deleting the data to the tables
        for table_name in TABLES[::-1]:
            delete_records_query = "DELETE FROM " + table_name
            cursor.execute(delete_records_query)
            cursor.commit()

        print(f"Test number {test_num} finished")
        print(f"*" * 50)