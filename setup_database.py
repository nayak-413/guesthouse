import pymysql


def create_database_if_not_exists():
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="nayak413",
        cursorclass=pymysql.cursors.Cursor,
    )
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS guesthouse")
    con.commit()
    con.close()


def init_db():
    # Create DB first
    create_database_if_not_exists()

    # Now connect to the newly created database and load init.sql
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="nayak413",
        database="guesthouse",
        cursorclass=pymysql.cursors.Cursor,
    )

    with open("db/init.sql", "r") as f:
        sql_statements = f.read().split(";")
        cur = con.cursor()
        for stmt in sql_statements:
            stmt = stmt.strip()
            if stmt:
                try:
                    cur.execute(stmt)
                except Exception as e:
                    print(f"Error executing: {stmt}\n{e}")
        con.commit()
        con.close()


# Run the full setup
init_db()
