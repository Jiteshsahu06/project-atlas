
# from app.agents.router import route_question
# from app.services.escalation_service import create_escalation


# def process_chat(client_id: str, question: str) -> dict:
#     category = route_question(question)

#     if category == "unsafe":
#         return {
#             "answer": "I cannot help with bypassing security or permissions.",
#             "category": category,
#             "confidence": 1.0,
#         }

#     if category == "out_of_scope":
#         return {
#             "answer": "Please ask a question related to the available market reports.",
#             "category": category,
#             "confidence": 0.9,
#         }

#     escalation_id = create_escalation(
#         client_id=client_id,
#         question=question,
#         reason="AI retrieval and answer generation are not integrated yet.",
#     )

#     return {
#         "answer": "I need more evidence to answer reliably. Your question has been escalated for review.",
#         "category": category,
#         "confidence": 0.0,
#         "escalation_id": escalation_id,
#     }


from app.agents.router import route_question
from app.services.escalation_service import create_escalation
from app.rag.embeddings import generate_embeddings
from app.rag.retriever import search_chunks


def process_chat(client_id: str, question: str) -> dict:
    category = route_question(question)

    if category == "unsafe":
        return {
            "answer": "I cannot help with bypassing security or permissions.",
            "category": category,
            "confidence": 1.0,
        }

    if category == "out_of_scope":
        return {
            "answer": "Please ask a question related to the available market reports.",
            "category": category,
            "confidence": 0.9,
        }

    try:
        query_embedding = generate_embeddings([question])[0]
        results = search_chunks(
            query_embedding=query_embedding,
            client_id=client_id,
            limit=10,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if category == "comparison" and len(documents) < 2:
            escalation_id = create_escalation(
                client_id=client_id,
                question=question,
                reason="Insufficient authorized evidence for comparison.",
            )
            return {
                "answer": (
                    "I cannot make a reliable comparison because "
                    "the available authorized reports do not provide "
                    "enough evidence for both sides."
                ),
                "category": category,
                "confidence": 0.0,
                "escalation_id": escalation_id,
            }


        if not documents:
            raise ValueError("No authorized evidence found.")

        citations = []
        context_parts = []

        for document, metadata in zip(documents, metadatas):
            report_id = metadata["report_id"]
            page = metadata["page"]

            context_parts.append(
                f"[{report_id}, page {page}]\n{document}"
            )
            citations.append(f"{report_id}, page {page}")

        context = "\n\n".join(context_parts)

        # Temporary extractive response: no LLM is connected yet.
        answer = (
            "Retrieved evidence from authorized reports:\n\n"
            + context
            + "\n\nSources: "
            + "; ".join(citations)
        )

        return {
            "answer": answer,
            "category": category,
            "confidence": 0.5,
        }

    except Exception:
        escalation_id = create_escalation(
            client_id=client_id,
            question=question,
            reason="No authorized evidence found or retrieval failed.",
        )

        return {
            "answer": (
                "I could not retrieve sufficient authorized evidence. "
                "Your question has been escalated for review."
            ),
            "category": category,
            "confidence": 0.0,
            "escalation_id": escalation_id,
        }
