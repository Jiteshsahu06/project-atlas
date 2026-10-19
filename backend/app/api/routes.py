
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.schemas.chat import ChatResponse


from app.database.connection import get_db_connection
from app.services.chat_service import process_chat

router = APIRouter()


class ChatRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=5000)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        result = process_chat(
            client_id=request.client_id,
            question=request.message,
        )

        cursor.execute(
            """
            INSERT INTO conversations
            (client_id, user_message, assistant_response)
            VALUES (%s, %s, %s)
            """,
            (
                request.client_id,
                request.message,
                result["answer"],
            ),
        )
        connection.commit()

        return result

    except Exception:
        if connection and connection.is_connected():
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to process the request.",
        )

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@router.get("/escalations")
def get_escalations(client_id: str):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, client_id, question, reason, status, created_at
            FROM escalations
            WHERE client_id = %s
            ORDER BY id DESC
            """,
            (client_id,),
        )

        return {"escalations": cursor.fetchall()}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch escalations.",
        )

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
