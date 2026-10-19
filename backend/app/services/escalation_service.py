
from app.database.connection import get_db_connection


def create_escalation(
    client_id: str,
    question: str,
    reason: str,
) -> int:
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO escalations
            (client_id, question, reason, status)
            VALUES (%s, %s, %s, 'open')
            """,
            (client_id, question, reason),
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        connection.close()
