import psycopg2

# 创建连接对象
conn = psycopg2.connect(database="db_tpcc", user="joe", password="Bigdata@123", host="1.94.201.203", port=26000)
cur = conn.cursor()

# 创建表
cur.execute("""
    CREATE TABLE IF NOT EXISTS S (
        Sno VARCHAR(10) NOT NULL,
        Cno VARCHAR(8) NOT NULL,
        Sname VARCHAR(100) NOT NULL,
        Gender VARCHAR(10) NOT NULL,
        Phone VARCHAR(11) NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Cla (
        Cno VARCHAR(8) NOT NULL,
        Cteacher VARCHAR(100) NOT NULL,
        Grade VARCHAR(100) NOT NULL,
        Number VARCHAR(10) NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Cou (
        Sno VARCHAR(10) NOT NULL,
        Sname VARCHAR(100) NOT NULL,
        Cou1 VARCHAR(100) NOT NULL,
        Cou2 VARCHAR(100) NOT NULL,
        Cou3 VARCHAR(100) NOT NULL
    );
""")

conn.commit()