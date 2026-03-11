import os
import ssl
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.cohere import CohereEmbedding

# פתרון SSL לנטפרי
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['CURL_CA_BUNDLE'] = ""

load_dotenv()


def load_with_metadata():
    all_docs = []

    # הגדרת הכלים והתיקיות שלהם כפי שמופיע במבנה הפרויקט שלך
    tools_setup = {
        "Claude": "./claude_docs",
        "Cursor": "./cursor_docs"
    }

    for tool_name, dir_path in tools_setup.items():
        if os.path.exists(dir_path):
            print(f"📂 טוען קבצים עבור {tool_name} מתיקיית {dir_path}...")
            # טעינה ספציפית לכל כלי
            reader = SimpleDirectoryReader(dir_path, required_exts=[".md"])
            docs = reader.load_data()

            # הוספת Metadata קריטי לכל מסמך כפי שנדרש במטלה
            for doc in docs:
                doc.metadata["tool"] = tool_name
                doc.metadata["source_type"] = "agentic_coding_docs"

            all_docs.extend(docs)

    return all_docs


# --- תחילת התהליך ---
documents = load_with_metadata()

print(f"✂️ מחלק {len(documents)} מסמכים ל-Chunks...")
parser = TokenTextSplitter(chunk_size=512, chunk_overlap=20)
nodes = parser.get_nodes_from_documents(documents)

print("🧬 מחבר את מודל ה-Embedding של Cohere...")
embed_model = CohereEmbedding(
    api_key=os.environ.get("COHERE_API_KEY"),
    model_name="embed-multilingual-v3.0"
)

print("💾 מעדכן את האינדקס המקומי בתיקיית 'storage'...")
index = VectorStoreIndex(nodes, embed_model=embed_model)
index.storage_context.persist(persist_dir="./storage")

print("✅ סיימנו! עכשיו לכל פיסת מידע יש Metadata של הכלי שיצר אותה.")