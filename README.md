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

Master Development Prompt: EmoShield Sentinel 🛡️
Project Overview

I have an existing Python cybersecurity project named EmoShield. I want to upgrade it into EmoShield Sentinel, an installable, real-time Windows desktop security application that detects suspicious messages, analyzes threats locally, and alerts users through native Windows notifications.

The application should run in the background and monitor supported messaging sources using authorized integrations. It should analyze accessible messages for phishing, scams, malicious links, suspicious Unicode characters, risky emoji patterns, and other potentially harmful content.

Important: Do not rebuild the entire project from scratch. First inspect my existing files, understand their responsibilities, and reuse the existing functionality wherever possible.

1. Existing Project Structure

My current project contains:

detector/
README.md
__init__.py
chat_analyzer.py
dashboard.py
report_generator.py
requirements.txt
risk_scoring.py
sample.txt
web_dashboard.py
__pycache__/

Some existing modules may include additional files such as detector/text_analysis.py.

Before writing code:

Inspect the entire repository.
Read the existing Python files and dependencies.
Identify the current detection algorithms, function signatures, imports, and data structures.
Identify reusable components and existing bugs.
Propose a migration plan that preserves backward compatibility.
Do not invent existing functions, classes, or file contents.
Ask for missing files only when they are genuinely needed.
2. Primary Objective

Transform EmoShield into a Windows-first desktop security application with these capabilities:

Real-time analysis of accessible incoming messages.
Local-first threat detection.
Native Windows desktop notifications.
Risk scoring from 0 to 100.
LOW, MEDIUM, and HIGH risk classifications.
Explanation of the indicators behind each alert.
Identification of the originating application and available message metadata.
A system-tray interface and background operation.
An installable Windows executable.
A modular architecture that supports additional messaging integrations.

The application should continue to support existing chat-file analysis, the terminal dashboard, the web dashboard, and report generation.

3. Technical Stack

Use the following technologies where appropriate:

Python 3.11 or newer.
Tkinter or another lightweight desktop GUI framework.
Windows-native notification APIs or a maintained Python notification library.
Windows notification-listener APIs for authorized notification access.
UI Automation only where supported, permitted, and necessary.
PyInstaller for packaging.
pytest for automated testing.
Existing EmoShield modules for detection and risk scoring.
SQLite only if persistent alert history is needed.
Optional FastAPI integration only if it provides a clear benefit.

Avoid unnecessary dependencies and complex microservices.

4. Real-Time Message Sources

Create a modular source-integration architecture.

Each source adapter should implement a common interface and return structured events containing the available fields:

Source application.
Message text or notification preview.
Sender or display name, if available.
Conversation identifier, if available.
Timestamp.
Message reference or navigation information, if available.
Source metadata and permission status.

Implement these integrations incrementally:

A. Windows notification monitoring

Use an authorized Windows notification-listener mechanism to analyze notification content that Windows exposes and the user has permitted the application to access.

Handle truncated notifications, missing content, unavailable sender information, and unsupported applications gracefully.

B. Clipboard monitoring

Provide an optional, clearly labeled development mode that analyzes copied text.

Do not represent clipboard monitoring as universal incoming-message monitoring. Do not assume clipboard text identifies its original application or sender.

C. Messaging integrations

Design adapters for supported messaging platforms and browser-based chat applications. Use official APIs, supported extensions, or authorized integration methods where available.

Do not bypass end-to-end encryption, application permissions, access controls, or security restrictions.

Do not claim that every message from every application can be captured. Display the supported sources and actual coverage clearly.

5. Detection Engine

Extend the existing detector modules instead of duplicating their functionality.

Implement or improve the following detectors:

Unicode security
Zero-width characters.
Bidirectional control characters.
Unexpected formatting characters.
Mixed-script text and potential homoglyph impersonation.
Suspicious Unicode normalization differences.

Preserve the original text and analyze a separate normalized representation.

URL security
URL parsing and hostname validation.
IP-address-based URLs.
Embedded credentials in URLs.
Punycode and internationalized domain indicators.
Suspicious URL structure.
Optional reputation checks through reputable threat-intelligence services.

Never automatically open suspicious URLs.

Treat unavailable reputation information as unknown rather than safe.

Phishing and scam detection
Credential and OTP requests.
Account suspension impersonation.
Suspicious payment requests.
Urgency and social-engineering language.
Prize and lottery scams.
Suspicious combinations of multiple indicators.
Emoji and text analysis
Suspicious emoji combinations.
Emoji-heavy messages.
Existing sentiment analysis.
Context-sensitive keyword detection.

Do not classify a message as malicious solely because it contains a particular word, emoji, or negative sentiment.

Machine learning

Design the system so a trained classifier can be added later.

Begin with a transparent rule-based baseline. Add a machine-learning classifier only when a suitable labeled dataset, training pipeline, and evaluation tests are available.

Never fabricate model accuracy, confidence, or training results.

6. Risk Scoring

Upgrade the existing risk_scoring.py rather than creating a competing scoring system.

Each analysis result should include:

Risk score from 0 to 100.
Risk level.
Threat category.
Detected indicators.
Evidence supporting the decision.
Model confidence, only when meaningfully available.
Recommended user action.
Analysis timestamp.
Source metadata.

Use configurable thresholds for LOW, MEDIUM, and HIGH risk.

Avoid double-counting correlated indicators. Keep evidence-based severity overrides separate from the aggregate score. Make clear that risk scores are heuristic estimates until calibrated against a labeled dataset.

7. Desktop Application

Build a polished Windows desktop interface with:

Application name: EmoShield Sentinel.
Start and stop monitoring controls.
Monitoring status.
Supported-source status.
Enable/disable controls for each source.
A live alert feed.
Search and filtering by risk level.
Alert details and detected indicators.
Source application and message timestamp.
Open-message action when the integration supports a reliable reference.
Settings for notification behavior and risk thresholds.
A button to analyze a message manually.
An option to export alert reports.

The app should minimize to the system tray when supported and allow the user to exit cleanly.

Monitoring must be visible, user-controlled, and disabled when required permissions are missing.

8. Windows Notifications

When a configured risk threshold is reached, show a native Windows notification.

Include:

EmoShield Sentinel branding.
Risk level.
Short threat description.
Source application when known.
One or two important detection indicators.

Avoid placing full private message contents in notifications by default.

Deduplicate repeated alerts, rate-limit notifications, and handle notification failures without crashing the application.

Do not claim that an alert was delivered if Windows rejected the notification.

9. Message Location and Context

Interpret message location as the location of the message within the digital application, not the sender's GPS location.

When available, show:

Application name.
Conversation or chat name.
Sender display name.
Timestamp.
Message reference.
Navigation action.

Do not fabricate metadata that an integration does not expose.

If the message cannot be linked to its original conversation, clearly label the source as unknown or partially identified.

10. Privacy and Security

Follow privacy-by-design principles:

Process message text locally by default.
Do not upload chat content to external AI services without explicit user consent.
Do not persist message contents unless necessary and clearly disclosed.
Avoid logging passwords, OTPs, or sensitive message contents.
Protect local configuration and any stored alert history.
Request only the permissions required by enabled integrations.
Provide clear monitoring and data-retention controls.
Do not silently capture keystrokes or screenshots.
Do not bypass security protections or application restrictions.
Handle malformed messages safely.
Do not execute links, attachments, or code extracted from messages.
11. Suggested Project Structure

Adapt this structure to the actual repository instead of blindly renaming existing files.

EmoShield/ ├── detector/ │ ├── existing detection modules │ ├── unicode_detector.py │ ├── url_detector.py │ └── phishing_detector.py ├── sources/ │ ├── init.py │ ├── base.py │ ├── clipboard_source.py │ └── windows_notifications.py ├── desktop/ │ ├── app.py │ ├── notifications.py │ └── tray.py ├── tests/ │ ├── test_detectors.py │ ├── test_risk_scoring.py │ └── test_sources.py ├── chat_analyzer.py ├── risk_scoring.py ├── dashboard.py ├── web_dashboard.py ├── report_generator.py ├── requirements.txt ├── run_desktop.bat ├── build.bat ├── README.md └── .gitignore

Keep the existing files where possible. Add new modules only when they provide a clear separation of responsibilities.

12. Packaging and Installation

Create:

run_desktop.bat to create or use a virtual environment and launch the application.
build.bat to build a Windows executable using PyInstaller.
An updated requirements.txt.
An updated README.md with installation and troubleshooting instructions.
A .gitignore that excludes virtual environments, caches, build outputs, secrets, and local databases.

If practical, create a proper Windows installer as a later milestone.

Document any Windows notification permissions, startup requirements, signing requirements, and packaging limitations.

Do not claim that the program has been compiled or tested unless the relevant commands were actually executed successfully.

13. Testing Requirements

Create automated tests for:

Ordinary benign messages.
Phishing and credential requests.
Suspicious URLs.
Invisible Unicode characters.
Bidirectional control characters.
Mixed-script and homoglyph examples.
False-positive cases.
Malformed message events.
Duplicate notification suppression.
Missing source metadata.
Risk-score boundaries.
Existing chat-file-analysis compatibility.

Use synthetic or appropriately licensed datasets. Do not include real private chat logs.

Measure precision, recall, F1 score, and false-positive rates when an evaluation dataset becomes available.

14. Implementation Workflow

Work incrementally in this order:

Phase 1: Repository audit

Inspect every existing source file.
Explain the current architecture.
Identify code worth reusing.
Present a concise implementation plan.

Phase 2: Core integration

Extend existing detectors and risk scoring.
Define a common message-event schema.
Add automated tests.
Preserve existing functionality.

Phase 3: Windows desktop application

Create the desktop interface.
Add opt-in clipboard monitoring.
Implement native notifications.
Add clean start/stop behavior.

Phase 4: Authorized message sources

Implement the Windows notification integration.
Verify the actual fields exposed by supported notifications.
Add platform-specific integrations individually.
Clearly document unsupported applications and coverage gaps.

Phase 5: Packaging

Create the executable build scripts.
Test the packaged application.
Document installation and troubleshooting.

Phase 6: Validation

Run the tests.
Fix integration errors.
Verify that the GUI and background threads terminate correctly.
Verify that notification failures do not crash the application.
Document remaining limitations.

At each phase, provide complete code for every new or modified file, its exact destination, installation commands, and verification steps.

If you can directly edit the repository, modify the files in place. Otherwise, provide complete, copyable files with their paths.

Do not replace my entire project with a generic demo. Do not leave essential functionality as unexplained pseudocode. Do not create fake integrations that claim to monitor all messaging applications.

Final Goal

Deliver a working, installable Windows desktop application named EmoShield Sentinel that reuses my existing Python project, analyzes messages available through authorized sources, detects suspicious content locally, explains its findings, and alerts the user with the available source and message location.

Begin by auditing the existing repository. Do not start implementing until you understand the current code and its dependencies.
