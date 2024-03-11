import re

def getSqlStatements() -> list[str]:
    global statements
    with open('src/sql/createTables.sql', 'r') as file:
        content = file.read()
    statements = [s.strip() for s in content.split(';') if s.strip()]
    return statements

def getTables(cursor) -> list[str]:
    tables = cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table';
    ''').fetchall()
    table_names = [table[0] for table in tables]
    return table_names

def getTableName(statement: str) -> str:
    """
    Get the table name from the statement.
    """
    pattern = re.compile(r"CREATE TABLE\s+['\"]?(\w+)['\"]?", re.IGNORECASE)
    match = pattern.search(statement)
    if match:
        return match.group(1)
    else:
        raise ValueError("Table name could not be extracted from SQL statement.")

def validateTable(cursor, statement, table_name):
    """
    Validate the table structure.
    """
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    current_statement = cursor.fetchone()[0]
    if current_statement != statement:
        print(f"Updating table {table_name}...")
        cursor.execute(f"DROP TABLE {table_name};")
        cursor.execute(statement + ';')

def verifyDB(conn):
    cursor = conn.cursor()
    try:
        statements = getSqlStatements()
        tables = getTables(cursor)

        added_tables = []
        for statement in statements:
            table_name = getTableName(statement)
            if table_name not in tables:
                print(f"Creating table {table_name}...")
                cursor.execute(statement + ';')
                added_tables.append(table_name)
            else:
                validateTable(cursor, statement, table_name)
        
        if added_tables:
            print("Added tables:", ', '.join(added_tables))
            conn.commit()
        else:
            print("Database tables are up to date.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()