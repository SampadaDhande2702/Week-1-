from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
import time

load_dotenv()

# Connect to Langfuse account
langfuse = Langfuse()

# Create a listener that records everything
langfuse_handler = CallbackHandler()

# 1. Load ChromaDB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# 2. Setup Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# 3. Question
question = "What is RAG?"

# 4. Retrieve chunks
docs = vectorstore.similarity_search(question, k=2)
context = "\n".join([doc.page_content for doc in docs])

# 5. Build prompt
prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
"""

# 6. Create a trace
trace = langfuse.trace(name="rag-query", input={"question": question})

# 7. Send to Gemini and measure time
start_time = time.time()

response = llm.invoke(
    [HumanMessage(content=prompt)],
    config={"callbacks": [langfuse_handler]}
)

latency = time.time() - start_time
answer = response.content
token_count = len(prompt.split()) + len(answer.split())

print(f"\n🙋 Question: {question}")
print(f"\n🤖 Answer: {answer}")
print(f"\n📄 Sources: {[doc.page_content for doc in docs]}")

# 8. Warning checks

# Check 1: High latency
if latency > 3:
    langfuse.score(trace_id=trace.id, name="latency-warning", value=0, comment=f"⚠️ Slow response! Took {latency:.2f}s")
    print(f"\n⚠️ WARNING: Response too slow! ({latency:.2f}s)")
else:
    langfuse.score(trace_id=trace.id, name="latency-warning", value=1, comment=f"✅ Fast response ({latency:.2f}s)")
    print(f"\n✅ Latency OK: {latency:.2f}s")

# Check 2: Answer too short
if len(answer.split()) < 10:
    langfuse.score(trace_id=trace.id, name="answer-length-warning", value=0, comment=f"⚠️ Answer too short! Only {len(answer.split())} words")
    print(f"\n⚠️ WARNING: Answer too short! ({len(answer.split())} words)")
else:
    langfuse.score(trace_id=trace.id, name="answer-length-warning", value=1, comment=f"✅ Answer length OK ({len(answer.split())} words)")
    print(f"\n✅ Answer Length OK: {len(answer.split())} words")

# Check 3: Too many tokens
if token_count > 500:
    langfuse.score(trace_id=trace.id, name="token-warning", value=0, comment=f"⚠️ Too many tokens! Used {token_count}")
    print(f"\n⚠️ WARNING: Too many tokens! ({token_count})")
else:
    langfuse.score(trace_id=trace.id, name="token-warning", value=1, comment=f"✅ Token count OK ({token_count})")
    print(f"\n✅ Token Count OK: {token_count}")

# Check 4: Low quality answer
bad_phrases = ["i don't know", "i am not sure", "i cannot answer", "no information"]
if any(phrase in answer.lower() for phrase in bad_phrases):
    langfuse.score(trace_id=trace.id, name="quality-warning", value=0, comment="⚠️ Low quality answer detected!")
    print(f"\n⚠️ WARNING: Low quality answer!")
else:
    langfuse.score(trace_id=trace.id, name="quality-warning", value=1, comment="✅ Answer looks good!")
    print(f"\n✅ Answer Quality OK")

# 9. Flush — send everything to Langfuse
langfuse.flush()
print("\n✅ Trace + Warnings sent to Langfuse!")