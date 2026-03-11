import os
import ssl
import json
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# 1. פתרון SSL לנטפרי וטעינת מפתחות
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['CURL_CA_BUNDLE'] = ""
load_dotenv()

# וידוא שהמפתח קיים
if not os.environ.get("OPENAI_API_KEY"):
    print("❌ שגיאה: לא נמצא OPENAI_API_KEY בקובץ .env")
    exit()


class Decision(BaseModel):
    id: str
    title: str
    summary: str
    tool: str
    file_path: str
    observed_at: str = Field(description="ISO date string")


class ExtractionSchema(BaseModel):
    decisions: List[Decision]
    rules: List[str] = Field(description="רשימת חוקי UI או הנחיות")


def run_extraction():
    print("🧠 מחלץ נתונים מובנים מהמסמכים (זה עשוי לקחת כמה שניות)...")

    llm = OpenAI(model="gpt-4o-mini")

    documents = SimpleDirectoryReader("./", recursive=True, required_exts=[".md"]).load_data()
    all_text = "\n".join([d.text for d in documents])

    # חילוץ מובנה
    structured_llm = llm.as_structured_llm(ExtractionSchema)
    response = structured_llm.complete(
        f"עבור על הטקסט הבא וחלץ ממנו רשימה של החלטות טכניות וחוקי עבודה/UI:\n{all_text}")

    # תיקון השמירה: לוקחים את הטקסט וטוענים אותו כ-JSON
    try:
        # בגרסאות מסוימות המידע נמצא בתוך response.text כסטרינג של JSON
        data_to_save = json.loads(response.text)
        with open("structured_data.json", "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        print("✅ הצלחנו! המידע המובנה נשמר ב-structured_data.json")
    except Exception as e:
        print(f"❌ שגיאה בשמירת ה-JSON: {e}")
        # גיבוי: פשוט שמרי את הטקסט הגולמי אם ה-Parsing נכשל
        with open("structured_data.json", "w", encoding="utf-8") as f:
            f.write(response.text)


if __name__ == "__main__":
    run_extraction()