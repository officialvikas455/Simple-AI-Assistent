import os
import numpy
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None


def get_embedding(text):
    global client

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY must be set to create embeddings.")

    model = os.getenv("EMBED_MODEL")
    if not model:
        raise ValueError("EMBED_MODEL must be set to create embeddings.")

    if client is None:
        client = OpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=api_key,
        )

    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding


def cosine_similarity(A, B):
    dot_prod = numpy.dot(A, B)
    norm_a = numpy.linalg.norm(A)
    norm_b = numpy.linalg.norm(B)
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Cosine similarity is undefined for a zero-length vector.")
    return dot_prod / (norm_a * norm_b)

#loads all text files from the specified folder (or KB_FOLDER environment variable) and returns a list of documents. Each document is a dictionary with source (filename) and text (file content).
def load_documents(folder=None):
    folder = folder or os.getenv("KB_FOLDER")
    if not folder:
        raise ValueError("KB_FOLDER must be set or passed to load_documents().")

    documents = []

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append(
                {
                    "source": filename,
                    "text":f.read(),
                }
            )

    return documents

#adds embeddings to each chunk in the list of chunks. Each chunk is a dictionary with source, chunk_id, text, and vector (embedding). The function returns the updated list of chunks.
def add_embeddings(chunks):
    for chunk in chunks:
        vector = get_embedding(chunk["text"])
        chunk["vector"] = vector

    return chunks

#search for the most relevant chunks based on the query and return the top_k results
def search(query, chunks, top_k=3):
    query_vector = get_embedding(query)

    results = []
    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["vector"])
        results.append(
            {
                "score" : float(score),
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "size": len(chunk["text"])
            }
        )

    results.sort(key=lambda rec: rec["score"], reverse=True)
    return results[:top_k]

#Takes one file and create multiple chunks based on the text content. Each chunk is a dictionary with source, chunk_id, and text. The function returns a list of chunks.
def chunk_document(document):
    chunks = []

    chunk_id = 0

    for part in document["text"].split("\n\n"):
        part = part.strip()
        if part:
            chunks.append(
                {
                    "source": document["source"],
                    "chunk_id": chunk_id,
                    "text": part,
                }
            )
            chunk_id += 1
    return chunks

#loads the knowledge base and create chunkss from each document
def create_chunks(folder=None):
    documents = load_documents(folder)
    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks


def save_vector_store(chunks, file_path=None):
    file_path = file_path or os.getenv("VECTOR_STORE_FILE")
    if not file_path:
        raise ValueError("VECTOR_STORE_FILE must be set or passed to save_vector_store().")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)


def load_vector_store(file_path=None):
    file_path = file_path or os.getenv("VECTOR_STORE_FILE")
    if not file_path:
        raise ValueError("VECTOR_STORE_FILE must be set or passed to load_vector_store().")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

    
def main():
    vector_store_file = os.getenv("VECTOR_STORE_FILE")
    if not vector_store_file:
        raise ValueError("VECTOR_STORE_FILE must be set.")

    if os.path.exists(vector_store_file):
        chunks = load_vector_store(vector_store_file)
        print(f"Loaded {len(chunks)} chunks from vector store file {vector_store_file}.")
    else:
        chunks = create_chunks()
        chunks = add_embeddings(chunks)
        save_vector_store(chunks, vector_store_file)
        print(f"Created and saved {len(chunks)} chunks to vector store file {vector_store_file}.")

    user_query = "What are the benefits of Maternity Leave?"
    results = search(user_query, chunks, 3) 

if __name__ == "__main__":
    main()