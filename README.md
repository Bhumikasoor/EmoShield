# EmoShield 🛡️

EmoShield is a **Cybersecurity + AI powered chat analyzer** built in Python.  
It detects hidden characters, suspicious emoji patterns, risky keywords, and sentiment tone in chats to identify **potentially harmful or malicious messages**.

---

## 🚀 Features

- **Hidden Character Detection**
  - Detects Zero-Width Joiners (ZWJ) and other invisible characters.
  - Flags suspicious Unicode tricks often used in phishing or smuggling.

- **Emoji Analyzer**
  - Detects risky emoji patterns (🌿 + 💨 → drug slang, 💊 + 🍬 → pills, etc.).
  - Flags emoji-only or emoji-heavy messages.
  - Calculates emoji anomaly scores.

- **Keyword Detection**
  - Flags suspicious terms related to violence, fraud, or drugs.
  - Weighted risk scoring (e.g., "kill" = HIGH risk, "weed" = MEDIUM).

- **Sentiment Analysis**
  - Detects emotional tone (Positive / Neutral / Negative).
  - Escalates risk when negative sentiment + violence keywords appear together.

- **Risk Scoring**
  - Unified scoring system (0–100).
  - Classifies messages into `LOW`, `MEDIUM`, or `HIGH` risk.

- **Chat File Analysis**
  - Analyze exported WhatsApp/Telegram chat logs.
  - Skips system headers and timestamps.
  - Exports results into **CSV/Excel**.
  - Prints a summary of overall chat risk.

- **Dashboard**
  - Interactive terminal dashboard built with `rich`.
  - Options to analyze single messages or entire chat files.

---

## 📂 Project Structure