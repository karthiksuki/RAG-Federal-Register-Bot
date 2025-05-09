import json
import aiomysql
import asyncio

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'db': 'federal_register',
    'autocommit': True
}

async def store_documents():
    with open("processed_documents.json", 'r') as f:
        documents = json.load(f)

    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cursor:
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents_fedral (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title TEXT,
                publication_date DATE,
                agency VARCHAR(255),
                url TEXT,
                pdf TEXT
            )
        """)
        for doc in documents:
            await cursor.execute("""
                INSERT INTO documents_fedral (title, publication_date, agency, url, pdf)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                doc.get('title'),
                doc.get('date'),
                doc.get('agency'),
                doc.get('url'),
                doc.get('pdf')
            ))
    conn.close()
    print(f"Stored in MySql DB")

if __name__ == "__main__":
    asyncio.run(store_documents())