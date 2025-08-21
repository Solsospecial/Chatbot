import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd
import uuid
from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import PyPDFLoader
client = chromadb.Client()
messages_collection = client.create_collection("messages_collection")
model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
def load_pdf(csv_file_path):
    try:
        # file_path = "upload/messages.csv"

        # messages_df = pd.read_csv(csv_file_path)
        # print(messages_df)
        # return messages_df
        loader = PyPDFLoader(file_path=csv_file_path)
        # CSVLoader(file_path=csv_file_path,encoding='utf-8')
        data = loader.load()
        print(len(data))
        return data
    # prometheus_fastapi_instrumentator'
# 
    except Exception as e:
        print(f"Error loading CSV file: {str(e)}")
        return None

def process_messages(data):
    if data is None:
        print("Nothing is present")
        return
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Prepare documents, embeddings, metadatas, and ids
    documents = []
    metadatas = []
    ids = []

    for index, document in enumerate(data):
        # Extract page content from the document
        content = document.page_content

        # Prepare metadata
        metadata = {
            'page_number': document.metadata.get('page_number', index + 1),
            # 'bot_id': str(bot_id)
        }
        metadatas.append(metadata)

        # Collect document content for embedding
        documents.append(content)
        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each chunk
    print(metadatas)
    print(documents)

    # Embed the documents
    embeddings = model.encode(documents, convert_to_tensor=True)

    # Add documents to the ChromaDB collection
    messages_collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),  # Convert embeddings to a list
        metadatas=metadatas,
        ids=ids,
    )

    print(f"Stored {len(documents)} document(s) in ChromaDB.")


    # for doc in data:
    #     messages_collection.add(
    #         ids=[str(uuid.uuid1())], metadatas=doc.metadata, documents=doc.page_content
    #         # embeddings=model.encode(doc.page_content).tolist()
    # )

    # Create a ChromaDB client
    

    # Create a collection
    

    # Initialize SentenceTransformer model
    

    # Prepare documents, embeddings, metadatas, and ids
#     documents = []
# # embeddings = []
#     metadatas = []
#     ids = []
#     # bot_id=1
#     for index, document in enumerate(data):
#         content_lines = document.page_content.split('\n')
        

#         # Iterate over each line in the document's content
#         for line in content_lines:
#             if line.startswith('CONVERSATION ID:'):
#                 conversation_id = line.split(': ')[1]
#             elif line.startswith('FROM:'):
#                 from_value = line.split(': ')[1]
#             elif line.startswith('TO:'):
#                 to_value = line.split(': ')[1]
#             elif line.startswith('CONTENT:'):
#                 content_value = line.split(': ')[1]
#         if content_value=='' or content_value==None:
#             pass
#         else:
#             print("Bot Id")
#             print(bot_id)
#         # Prepare metadata
#             metadata = {
#                 'CONVERSATION ID': conversation_id,
#                 'FROM': from_value,
#                 'TO': to_value,
#                 # 'CONTENT': content_value,
#                 'bot_id': str(bot_id)  # Replace 'your_bot_id' with the actual ID
#             }
#             metadatas.append(metadata)
#             concatenated_text = f"From: {from_value}, To: {to_value}, Content: {content_value}"

#             # Collect document content for embedding
#             documents.append(concatenated_text)
#             # print(content_lines)
#             ids.append(str(index + 1))
#             print(content_value)

#     embedding=model.embed_documents(documents)
#     # embeddings.append(embedding)

#     print(metadatas)

#         # Add documents to the collection
#     messages_collection.add(
#             documents=documents,
#             embeddings=embedding,
#             metadatas=metadatas,
#             ids=ids,
#     )
        
def add_linkedin_messages(pdf_file_path):
    # Load messages from CSV
    print("Loadng Messages.")
    messages_df = load_pdf(pdf_file_path)
    

    # Process messages and add to ChromaDB collection
    process_messages(messages_df)
    print("Processing")



