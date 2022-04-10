import psycopg2
import sys
sys.path.insert(1, '/Users/constantion/Desktop/CRYPTO BOT/Crypto_bot_telegram')

import test
import settings

def connect_db():
    try:
        connection = psycopg2.connect(
            host = settings.host,
            database = settings.db_name,
            user = settings.user,
            password = settings.password,
            port = settings.port_id
        )
        # Call IT one Time That's it
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )

            print(f"Server version: {cursor.fetchone()}")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")