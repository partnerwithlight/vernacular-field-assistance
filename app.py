import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import pandas as pd
import os

# --- INITIALIZE GOOGLE GENAI CLIENT ---
# This automatically reads the GEMINI_API_KEY environment variable
client = genai.Client()

DB_FILE = "api_field_ledger.csv"

# Initialize local CSV database file if it doesn't exist
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Timestamp", "Original Input", "Category", "English Summary", "Action/Value"])
    df.to_csv(DB_FILE, index=False)

# --- DEFINE STRICT OUTPUT SCHEMA ---
# Pydantic forces the API to return exact structured JSON without markdown junk
class AssistantAnalysis(BaseModel):
    explanation: str = Field(description="Clear English translation and summary of what the user meant.")
    category: str = Field(description="Must be exactly one of: 'Transaction', 'Inventory', 'Inquiry', 'Alert'.")
    action_value: str = Field(description="The specific currency amount, item count, or core request extracted.")

# --- STREAMLIT UI ---
st.set_page_config(page_title="Vernacular Field Assistant (API)", page_icon="🌾", layout="wide")

st.title("🌾 Vernacular Field Assistant")
st.caption("Cloud-powered translation & automated data ledger using the Google GenAI SDK")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Field Input")
    # Let the user choose their preferred input method
    input_method = st.radio("Choose Input Method:", ["🎙️ Voice Recording", "⌨️ Text / Presets"], horizontal=True)
    
    user_audio = None
    user_input = ""
    
    if input_method == "🎙️ Voice Recording":
        st.write("Click below to record your voice (Speak in Pidgin, Hausa, Igbo, Yoruba, etc.):")
        # Native Streamlit audio input widget
        user_audio = st.audio_input("Record audio note")
        
    else:
        if "note_text" not in st.session_state:
            st.session_state.note_text = ""

        def set_text(text):
            st.session_state.note_text = text

        # Row 1
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            st.button("🇳🇬 Pidgin: Trade", use_container_width=True,
                      on_click=set_text,
                      args=("Oga Emeka collect 4 bags of garri on credit, he say he go pay 25000 next week Friday.",))
        with row1_col2:
            st.button("🇳🇬 Hausa: Supply", use_container_width=True,
                      on_click=set_text,
                      args=("Mun kawo buhun shinkafa guda goma yau, amma guda biyu sun jika saboda ruwan sama.",))
        with row1_col3:
            st.button("🇳🇬 Igbo: Expense", use_container_width=True,
                      on_click=set_text,
                      args=("E mefuru m puku kwuru puku naira iri abụọ iji zụta fatịlaịza maka ugbo anyị taa.",))

        # Row 2
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        with row2_col1:
            st.button("🇳🇬 Yoruba: Inventory", use_container_width=True,
                      on_click=set_text,
                      args=("A ti ta apo efo ati isu mẹwa loni ni ọjà, owo ti wọle to 15,000 naira.",))
        with row2_col2:
            st.button("🇳🇬 Fulani: Alert", use_container_width=True,
                      on_click=set_text,
                      args=("Ngelu durngol ngol hooti, kono nagge woore majji haa ladde.",))
        with row2_col3:
            st.button("🔄 Clear Input", use_container_width=True,
                      on_click=set_text, args=("",))

        user_input = st.text_area(
            "Enter mixed language / vernacular notes:",
            key="note_text",
            height=120,
    )
    
    submit_btn = st.button("Process & Log via API", type="primary")


with col2:
    st.subheader("📊 Assistant Insights")

    has_input = bool(user_input.strip()) or user_audio is not None

    if submit_btn and has_input:
        with st.spinner("Calling API..."):
            try:
                system_prompt = (
                    "You are an expert Vernacular Field Assistant for local market traders and farmers. "
                    "The user will input text or speech containing regional dialects, slang, or mixed English "
                    "(Pidgin, Hausa, Igbo, Yoruba, Fulani, etc.). "
                    "Translate it and classify it accurately."
                )

                # Build contents depending on input method
                if user_audio is not None:
                    audio_bytes = user_audio.getvalue()
                    contents = [
                        "Transcribe and analyze this voice note from a field trader/farmer.",
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=user_audio.type or "audio/wav",
                        ),
                    ]
                    original_input = "[Voice note]"
                else:
                    contents = f"User Input: {user_input}"
                    original_input = user_input

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        response_mime_type="application/json",
                        response_schema=AssistantAnalysis,
                        temperature=0.2,
                    ),
                )

                result: AssistantAnalysis = response.parsed

                st.success("API Response Received!")
                st.markdown(f"**💡 English Translation:** {result.explanation}")
                st.markdown(f"**🏷️ Category:** `{result.category}`")
                st.markdown(f"**🔢 Extracted Value/Action:** `{result.action_value}`")

                new_row = {
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Original Input": original_input,
                    "Category": result.category,
                    "English Summary": result.explanation,
                    "Action/Value": result.action_value,
                }

                df_ledger = pd.read_csv(DB_FILE)
                df_ledger = pd.concat([df_ledger, pd.DataFrame([new_row])], ignore_index=True)
                df_ledger.to_csv(DB_FILE, index=False)

            except Exception as e:
                st.error(f"API Error occurred: {e}")
    elif submit_btn:
        st.warning("Please record a voice note or enter some text first.")

# --- LEDGER VISUALIZATION ---
st.divider()
st.subheader("🗃️ Field Ledger (Saved to Disk)")
if os.path.exists(DB_FILE):
    current_ledger = pd.read_csv(DB_FILE)
    if not current_ledger.empty:
        st.dataframe(current_ledger.tail(10), use_container_width=True)
