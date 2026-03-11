import os
import ssl
import json
import gradio as gr
from dotenv import load_dotenv

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step, Event
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.utils.workflow import draw_all_possible_flows

# פתרון SSL לנטפרי
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['CURL_CA_BUNDLE'] = ""
load_dotenv()

# 1. טעינת בסיס הנתונים (Vector Store)
embed_model = CohereEmbedding(api_key=os.environ.get("COHERE_API_KEY"), model_name="embed-multilingual-v3.0")
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context, embed_model=embed_model)
vector_query_engine = index.as_query_engine(llm=OpenAI(model="gpt-3.5-turbo"))

# 2. הגדרת "כלים" עבור ה-Router
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="שימושי לשאלות כלליות על תוכן המסמכים וחיפוש סמנטי."
)


# --- הגדרת ה-Workflow עם ה-Router ---
class AgenticRAGWorkflow(Workflow):

    @step
    async def route_query(self, ev: StartEvent) -> Event:
        query = ev.get("query")

        # לוגיקת ה-Router: האם זו שאלה למבנה הנתונים המובנה (JSON) או לוקטורים?
        # אנחנו משתמשים ב-LLM כדי להחליט (זה ה-Router האמיתי)
        llm = OpenAI(model="gpt-3.5-turbo")
        prompt = f"האם השאלה הבאה דורשת רשימה של החלטות/חוקים או חיפוש חופשי בטקסט? ענה ב'structured' או 'semantic'. השאלה: {query}"
        decision = llm.complete(prompt).text.strip().lower()

        return Event(query=query, selection=decision)

    @step
    async def execute_step(self, ev: Event) -> StopEvent:
        query = ev.get("query")
        selection = ev.get("selection")

        if "structured" in selection:
            print("📊 ה-Router בחר: שליפה מובנית מ-JSON")
            try:
                with open("structured_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                # שליחת המידע ל-LLM שינסח תשובה יפה מה-JSON
                llm = OpenAI(model="gpt-3.5-turbo")
                response = llm.complete(f"בהתבסס על הנתונים הבאים: {json.dumps(data)}, ענה על השאלה: {query}")
                return StopEvent(result=str(response))
            except Exception as e:
                return StopEvent(result=f"שגיאה בשליפת נתונים מובנים: {e}")

        print("🔍 ה-Router בחר: חיפוש סמנטי ב-Vector Store")
        response = vector_query_engine.query(query)
        return StopEvent(result=str(response))
# זה ייצור קובץ HTML עם תרשים של ה-Workflow שלך
# הרצה
rag_workflow = AgenticRAGWorkflow(timeout=60)


async def chat_fn(message, history):
    return await rag_workflow.run(query=message)

# הפקודה הזו סורקת את המחלקה ומייצרת את התרשים
draw_all_possible_flows(rag_workflow, filename="workflow_graph.html")

# פשוט תחליפי את השורה הזו
gr.ChatInterface(
    fn=chat_fn,
    title="Agentic RAG Assistant - תיעוד החלטות טכניות",
    description="מערכת חכמה לניהול ותשאול החלטות טכניות וחוקי UI מתוך התיעוד."
).launch()