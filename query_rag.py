from dataclasses import dataclass, asdict
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_chroma_db import get_chroma_db
import json
import argparse


PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
---
Answer the question based on the above context: {question}
"""

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]

def query_rag(query_text: str) -> QueryResponse:
    db = get_chroma_db()

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)
    model = OllamaLLM(model="llama3.1")
    response = model.invoke(prompt)
    response_text = response  # Since `invoke` returns a string
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    # print(f"Response: {response_text}\nSources: {sources}")
    response =  QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )
    response_json = json.dumps(asdict(response))
    print(response_json)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)