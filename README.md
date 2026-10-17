🌾 Vernacular Field Assistant

A cloud-powered tool that translates voice notes and text written in Nigerian vernacular languages (Pidgin, Hausa, Igbo, Yoruba, Fulani and mixed English) into clear English, classifies what was said, and automatically saves every entry to a searchable ledger.

⚠️ This is a basic version (prototype / MVP). It is built to prove the concept and can be extended into a full product. See Roadmap.

Why this instead of normal Google Translate?

Google Translate converts text from one language to another, and then it's gone. This project goes further:

	Google Translate	Vernacular Field Assistant
Translates vernacular to English	✅	✅
Accepts voice notes directly	Limited	✅
Understands trade/farm context	❌	✅
Classifies the message (Transaction, Inventory, Inquiry, Alert)	❌	✅
Extracts key values (amounts, quantities, requests)	❌	✅
Logs every conversation to a ledger	❌	✅

The key advantage is the log. Every translated note is stored with a timestamp, the original input, its category, an English summary and the extracted value. For a market trader or farmer, that turns casual conversations into a record they can review later, such as who owes what, what stock came in, and what was spent. Nothing is lost once the chat is closed.

Features
🎙️ Voice input: record a note directly in the browser
⌨️ Text input: type your own note or use quick demo presets (Pidgin, Hausa, Igbo, Yoruba, Fulani)
🌍 Translation and summary in plain English
🏷️ Automatic categorisation: Transaction, Inventory, Inquiry or Alert
🔢 Value extraction: pulls out amounts, item counts or the core request
🗃️ Persistent ledger: every entry is saved to a CSV file and the 10 most recent are shown in the app
📐 Structured output: responses are forced into a strict JSON schema, so the data is always clean and consistent
Tech Stack
Layer	Technology
Language	Python 3
Front end / UI	Streamlit
AI model	Google Gemini (via the Google GenAI SDK, google-genai)
Data validation / structured output	Pydantic
Data handling and storage	pandas with a local CSV file
How It Works
The user records a voice note or enters text.
The input is sent to Gemini with a system prompt tuned for regional dialects and slang.
Gemini returns a structured JSON response (English explanation, category, extracted value) validated by a Pydantic schema.
The result is shown in the UI and appended to api_field_ledger.csv.
The ledger is displayed at the bottom of the page.
Getting Started
1. Clone the project
bash
git clone <your-repo-url>
cd <your-project-folder>
2. Install dependencies
bash
pip install streamlit google-genai pydantic pandas
3. Set your Gemini API key

Get a key from Google AI Studio, then set it as an environment variable:

bash
# macOS / Linux
export GEMINI_API_KEY="your-api-key"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key"
4. Run the app
bash
streamlit run app.py

(Replace app.py with your file name.)

Project Structure
.
├── app.py                  # Main Streamlit application
├── api_field_ledger.csv    # Auto-generated ledger (created on first run)
└── README.md
Ledger Format
Column	Description
Timestamp	When the entry was logged
Original Input	The text entered (or [Voice note] for audio)
Category	Transaction, Inventory, Inquiry or Alert
English Summary	Clear English translation of what was said
Action/Value	Extracted amount, quantity or request
Current Limitations

This is a basic version, so keep these in mind:

No user accounts: everyone shares the same ledger
Storage is a local CSV file, which is not suited to many users or large volumes
Voice notes are logged as [Voice note] rather than a transcript
Translation accuracy for less-resourced languages can vary, so important records should be reviewed
No editing or deleting of ledger entries from the UI
Roadmap

This project is designed to grow. Planned and possible improvements:

👤 Account management: sign-up/login so each trader or farmer has a private ledger
🗄️ Proper database: move from CSV to SQLite, PostgreSQL or Firebase
📝 Voice transcripts: store the original spoken text in the ledger
✏️ Edit and delete entries, plus search and filters
📤 Export to Excel/PDF and generate daily or weekly summaries
📊 Dashboards: totals for sales, expenses and stock over time
📱 Mobile-friendly or WhatsApp integration for easier field use
🌐 More languages and dialects
License

Add your preferred license here (e.g. MIT).
