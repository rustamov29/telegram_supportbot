"""# database.py
import aiosqlite

DB_NAME = "super_kitobxon.db"

async def init_db(initial_owner_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                role TEXT NOT NULL DEFAULT 'user',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, role) VALUES (?, 'owner')
        ''', (initial_owner_id,))
        
        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
        await db.commit()

async def get_user_role(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT role FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 'user'

async def set_user_role(user_id: int, role: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO users (user_id, role) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET role = excluded.role
        ''', (user_id, role))
        await db.commit()

async def transfer_ownership(old_owner_id: int, new_owner_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET role = 'admin' WHERE user_id = ?", (old_owner_id,))
        await db.execute('''
            INSERT INTO users (user_id, role) VALUES (?, 'owner')
            ON CONFLICT(user_id) DO UPDATE SET role = 'owner'
        ''', (new_owner_id,))
        await db.commit()

async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def get_admins_and_owner():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users WHERE role IN ('owner', 'admin')") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def get_stats():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c1:
            total_users = (await c1.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'") as c2:
            total_admins = (await c2.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM feedbacks") as c3:
            total_feedbacks = (await c3.fetchone())[0]
        return total_users, total_admins, total_feedbacks

async def add_feedback(user_id: int, text: str) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('INSERT INTO feedbacks (user_id, text) VALUES (?, ?)', (user_id, text))
        await db.commit()
        return cursor.lastrowid """








import aiosqlite

DB_NAME = "database.db"

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        # Users jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                role TEXT DEFAULT 'user'
            )
        """)
        # Teacher ratings jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS teacher_ratings (
                user_id INTEGER,
                teacher_name TEXT,
                rating INTEGER,
                comment TEXT,
                PRIMARY KEY (user_id, teacher_name)
            )
        """)
        
        # Eski bazaga 'comment' ustunini majburiy qo'shish
        try:
            await db.execute("ALTER TABLE teacher_ratings ADD COLUMN comment TEXT")
        except Exception:
            pass  # Agar ustun allaqachon bo'lsa, xatoni o'tkazib yuboradi

        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def get_user_role(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT role FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 'user'

async def set_user_role(user_id: int, role: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO users (user_id, role) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET role = ?", (user_id, role, role))
        await db.commit()

async def save_teacher_rating(user_id: int, teacher_name: str, rating: int, comment: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO teacher_ratings (user_id, teacher_name, rating, comment)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, teacher_name) DO UPDATE SET rating = ?, comment = ?
        """, (user_id, teacher_name, rating, comment, rating, comment))
        await db.commit()

# TO'G'RILANGAN FUNKSIYA:
async def get_teacher_stats(teacher_name: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT AVG(rating), COUNT(rating) FROM teacher_ratings WHERE teacher_name = ?",
            (teacher_name,)
        ) as cursor:
            row = await cursor.fetchone()
            avg_rating = row[0] if row and row[0] is not None else 0.0
            count = row[1] if row and row[1] is not None else 0
            return avg_rating, count

async def get_user_count() -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def get_admin_count() -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users WHERE role IN ('admin', 'owner')") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_total_feedback_count() -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM teacher_ratings") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_all_admins():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users WHERE role IN ('admin', 'owner')") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


