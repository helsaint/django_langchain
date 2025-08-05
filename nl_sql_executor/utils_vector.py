import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain import hub
from langchain_deepseek import ChatDeepSeek
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    prompt = hub.pull("rlm/rag-prompt")
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device":"cpu"}
    )

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=os.environ["DB_COLLECTION_NAME"],
    connection=os.environ["DATABASE_URL"],
    use_jsonb=True,
)

llm = ChatDeepSeek(
    temperature=0,
    model="deepseek-chat",
    #model_kwargs={"model_provider":"deepseek"},
    max_tokens=500, 
    api_key=os.environ["DEEPSEEK_API_KEY"]
    )

def create_vector_chain():
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    return graph