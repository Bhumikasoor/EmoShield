import streamlit as st
import pandas as pd
import io
from collections import Counter
import plotly.express as px
from risk_scoring import calculate_risk

# Extra imports for docx/pdf
from docx import Document
import PyPDF2

st.set_page_config(page_title="EmoShield Dashboard 🛡️", layout="wide")

st.title("🛡️ EmoShield — Interactive Chat Risk Analyzer")

st.markdown("""
Upload your chat files in **any format** (TXT, CSV, Excel, Word, PDF) or analyze a single message.  
EmoShield detects **hidden chars, emoji abuse, risky keywords, sentiment, and more**.
""")

# --- Option Selector ---
mode = st.radio("Select Mode:", ["Single Message", "Chat File Upload"])

# --- Option A: Single Message ---
if mode == "Single Message":
    msg = st.text_area("✍️ Enter your message here:", height=100)

    if st.button("Analyze Message"):
        if msg.strip():
            result = calculate_risk(msg)

            st.subheader("📊 Message Analysis Result")
            st.write(f"**Message:** {result['text']}")
            st.write(f"**Risk Level:** {result['risk_level']}")
            st.write(f"**Total Score:** {result['total_score']}")
            st.write(f"**Keywords:** {', '.join(result['keywords']) if result['keywords'] else 'None'}")
            st.write(f"**Sentiment:** {result['sentiment']['label']}")
            st.write(f"**Emoji Risk:** {result['emoji_report']['risk']}")
        else:
            st.warning("⚠️ Please enter a message before analyzing.")

# --- Option B: File Upload ---
elif mode == "Chat File Upload":
    uploaded = st.file_uploader("📂 Upload a chat file", type=["txt", "csv", "xlsx", "xls", "docx", "pdf"])

    if uploaded:
        lines = []

        # --- Handle different file formats ---
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
            lines = df[df.columns[0]].astype(str).tolist()

        elif uploaded.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded)
            lines = df[df.columns[0]].astype(str).tolist()

        elif uploaded.name.endswith(".txt"):
            lines = uploaded.read().decode("utf-8").splitlines()

        elif uploaded.name.endswith(".docx"):
            doc = Document(uploaded)
            lines = [p.text for p in doc.paragraphs if p.text.strip()]

        elif uploaded.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    lines.extend(text.splitlines())

        # --- Run analysis ---
        results = []
        for i, raw in enumerate(lines, 1):
            if not raw.strip():
                continue
            r = calculate_risk(raw)
            results.append({
            "line": i,
            "message": r["text"],
            "total_score": r["total_score"],
            "risk_level": r["risk_level"],
            "keywords": ", ".join(r["keywords"]) if r["keywords"] else "None",
            "sentiment": r["sentiment"]["label"],
            "emoji_risk": r["emoji_report"]["risk"]
            })

        if results:
            df_results = pd.DataFrame(results)

            st.subheader("📊 Chat File Analysis Results")
            st.dataframe(df_results, use_container_width=True)

            # ----- Charts -----
            st.markdown("### 📈 Visual Insights")

            # Risk Level Pie
            risk_counts = df_results["risk_level"].value_counts().reset_index()
            risk_counts.columns = ["risk_level", "Count"]
            fig_pie = px.pie(risk_counts, names="risk_level", values="Count",
                             title="risk_level Distribution", color="risk_level",
                             color_discrete_map={"LOW": "green", "MEDIUM": "orange", "HIGH": "red"})
            st.plotly_chart(fig_pie, use_container_width=True)

            # Keyword Frequency
            all_keywords = []
            for kw in df_results["keywords"]:
                if kw != "None":
                    all_keywords.extend([k.strip() for k in kw.split(",")])
            if all_keywords:
                from collections import Counter
                kw_counts = Counter(all_keywords)
                df_kw = pd.DataFrame(kw_counts.items(), columns=["Keyword", "Count"]).sort_values(by="Count", ascending=False)
                fig_bar = px.bar(df_kw.head(10), x="Keyword", y="Count", title="Top Keywords Detected", color="Count")
                st.plotly_chart(fig_bar, use_container_width=True)

            # Sentiment Distribution
            sentiment_counts = df_results["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            fig_sentiment = px.bar(sentiment_counts, x="Sentiment", y="Count",
                                   title="Sentiment Distribution", color="Sentiment")
            st.plotly_chart(fig_sentiment, use_container_width=True)

            # ----- Downloads -----
            st.markdown("### 💾 Export Reports")

            # CSV
            csv_buffer = io.StringIO()
            df_results.to_csv(csv_buffer, index=False)
            st.download_button("⬇️ Download CSV Report", data=csv_buffer.getvalue(),
                            file_name="EmoShield_Report.csv", mime="text/csv")

            # Excel
            xlsx_buffer = io.BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
                df_results.to_excel(writer, index=False, sheet_name="Report")
            st.download_button("⬇️ Download Excel Report", data=xlsx_buffer.getvalue(),
                            file_name="EmoShield_Report.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            # DOCX (Word Report with charts)
            from report_generator import generate_doc_report
            docx_buffer = generate_doc_report(results)
            st.download_button("⬇️ Download Word Report", data=docx_buffer,
                   file_name="EmoShield_Report.docx",
                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
