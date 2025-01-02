from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def get_prompt(query_text, vector_store_location):
    # Prepare the DB.
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    new_vector_store = FAISS.load_local(
        vector_store_location, embeddings, allow_dangerous_deserialization=True
    )
    results = new_vector_store.similarity_search_with_score(query_text)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    return prompt, sources

def ask(chat_history):
    model = ChatOpenAI(model="gpt-4o-mini")
    ai_msg = model.invoke(chat_history)
    response_text = ai_msg.content
    return response_text
