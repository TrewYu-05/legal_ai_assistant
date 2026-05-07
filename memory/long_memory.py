import sqlite3

DB_NAME = "memory.db"

# =========================
# 初始化数据库
# =========================

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (

        thread_id TEXT,
        key TEXT,
        value TEXT
    )
    """)

    conn.commit()

    conn.close()

# =========================
# 保存记忆
# =========================

def save_memory(thread_id, key, value):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # 先删除旧数据
    cursor.execute("""
    DELETE FROM user_memory
    WHERE thread_id=? AND key=?
    """, (thread_id, key))

    # 插入新数据
    cursor.execute("""
    INSERT INTO user_memory
    VALUES (?, ?, ?)
    """, (thread_id, key, value))

    conn.commit()

    conn.close()

# =========================
# 获取记忆
# =========================

def get_memory(thread_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT key, value
    FROM user_memory
    WHERE thread_id=?
    """, (thread_id,))

    rows = cursor.fetchall()

    conn.close()

    memory = {}

    for key, value in rows:
        memory[key] = value

    return memory

# =========================
# 获取单个记忆
# =========================

def get_single_memory(thread_id, key):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT value
    FROM user_memory
    WHERE thread_id=? AND key=?
    """, (thread_id, key))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None