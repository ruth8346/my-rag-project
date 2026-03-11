<div dir="rtl">

# 🤖 Agentic RAG Assistant - תיעוד החלטות טכניות

מערכת **RAG (Retrieval-Augmented Generation)** מתקדמת המיועדת לניהול, אינדוקס ותשאול תיעוד טכני שנוצר על ידי סוכני פיתוח כמו **Claude** ו-**Cursor**. המערכת מאחדת ידע ממקורות שונים ומאפשרת הפקת תובנות באמצעות ניתוב (**Routing**) חכם בין חיפוש סמנטי לשליפת נתונים מובנים.

---

## 🎯 מטרת הפרויקט
בסביבת פיתוח מודרנית, החלטות טכניות וחוקי UI מתפזרים בין קבצי Markdown שנוצרו על ידי AI. פרויקט זה נועד לרכז את המידע הזה ולאפשר לסוכן חכם לענות על שאלות מורכבות תוך שמירה על הקשר (**Context**) והפרדה בין מקורות הידע (**Metadata**).

---

## 🛠 סט טכנולוגי
* **Framework:** LlamaIndex (Workflows)
* **Embeddings:** Cohere (multilingual-v3.0)
* **LLM:** OpenAI (GPT-3.5-turbo & GPT-4o-mini)
* **User Interface:** Gradio

---

## 🧩 ארכיטקטורה ומימוש (שלבי הפרויקט)

### שלב א': Ingestion & Metadata
* טעינת נתונים משני מקורות נפרדים: `claude_docs` ו-`cursor_docs`.
* הוספת **Metadata** לכל מסמך המזהה את הכלי המקורי.
* יצירת Vector Store מקומי לשמירה על פרטיות ויעילות.

### שלב ב': Event-Driven Workflow
* מימוש זרימת עבודה מבוססת **Events** באמצעות LlamaIndex Workflows.
* הגדרת שלבי ולידציה על קלט המשתמש ואיכות התשובה (Confidence check).

### שלב ג': Data Extraction & Routing
* **Extraction:** חילוץ אוטומטי של החלטות טכניות וחוקי UI לתוך קובץ `structured_data.json` בסכימה מובנית.
* **Routing:** שימוש ב-LLM כנתב חכם המנתב שאילתות בין חיפוש וקטורי לשליפת נתונים מובנים מה-JSON.

---

## 🚀 הוראות הרצה
1.  **התקנת דרישות מערכת:**
    ```bash
    pip install llama-index llama-index-embeddings-cohere llama-index-llms-openai gradio python-dotenv llama-index-utils-workflow pyvis
    ```
2.  **הגדרת משתני סביבה:** צרו קובץ `.env` והזינו את המפתחות: `OPENAI_API_KEY`, `COHERE_API_KEY`.
3.  **בניית האינדקס:** הריצו `python ingest.py`.
4.  **חילוץ נתונים מובנים:** הריצו `python extract_data.py`.
5.  **הפעלת הסוכן:** הריצו `python app.py`.

---

## 📊 ויזואליזציה
עם הרצת האפליקציה, נוצר באופן אוטומטי קובץ בשם **`workflow_graph.html`**. קובץ זה מכיל תרשים זרימה אינטראקטיבי המציג את שלבי ה-Workflow והניתוב של הסוכן.

## 🧠 דוגמאות לשאלות שהסוכן יודע לענות עליהן
* **שאלות מובנות:** "מהן כל ההחלטות הטכניות שהתקבלו?"
* **שאלות סמנטיות:** "איך עובד מנגנון ה-Authentication בפרויקט?"
* **שאלות Metadata:** "אילו חוקי UI הוגדרו ספציפית על ידי Claude?"

---
**הוגש במסגרת קורס RAG - מלכה ברוק.**

</div>