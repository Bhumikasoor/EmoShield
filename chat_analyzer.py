import csv
from collections import Counter
from risk_scoring import calculate_risk
from detector.utils import unescape_unicode_escapes, remove_zero_width
from detector.text_analysis import detect_keywords
from report_generator import generate_doc_report

# Platform-specific system message patterns
PLATFORM_PATTERNS = {
    "whatsapp": [
        "This message was deleted",
        "joined using this group link",
        "left",
        "added",
        "removed"
    ],
    "telegram": [
        "joined the chat",
        "left the chat",
        "pinned a message",
        "unpinned a message"
    ],
    "messenger": [
        "created the group",
        "added",
        "removed",
        "left the conversation"
    ],
    "signal": [
        "joined the group",
        "left the group",
        "changed the group name"
    ]
}

def is_system_message(line: str, system_patterns=None) -> bool:
    """Check if line is empty or matches system patterns."""
    if not line.strip():
        return True
    if system_patterns:
        for pattern in system_patterns:
            if pattern.lower() in line.lower():
                return True
    return False

def merge_multiline_messages(lines):
    """Merge consecutive lines that are part of the same message."""
    merged = []
    buffer = ""
    for line in lines:
        if line.strip() == "":
            continue  # skip empty lines
        # Heuristic: if line starts with date/time pattern, start new message
        if buffer:
            buffer += " " + line.strip()
        else:
            buffer = line.strip()
        merged.append(buffer)
        buffer = ""
    return merged

def analyze_chat(file_path: str, platform: str = None, output_path: str = "chat_report.csv", summary_path: str = None):
    results = []

    system_patterns = PLATFORM_PATTERNS.get(platform.lower(), []) if platform else []

    with open(file_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # Merge multi-line messages
    lines = merge_multiline_messages(raw_lines)

    for i, line in enumerate(lines, 1):
        if is_system_message(line, system_patterns):
           continue  # skip system messages

        # convert escaped \u200d etc. into actual chars
        line = unescape_unicode_escapes(line)

        # keep a cleaned version without hidden chars for keyword detection
        clean_for_keywords = remove_zero_width(line)

        # run scoring on the original (with hidden chars intact)
        result = calculate_risk(line)

        # recompute keywords on the clean text (avoid false positives)
        result["keywords"] = detect_keywords(clean_for_keywords)

        results.append({
            "line": i,
            "message": line,
            "risk_level": result["risk_level"],
            "total_score": result["total_score"],
            "keywords": ", ".join(result["keywords"]) or "None",
            "sentiment": result["sentiment"]["label"],
            "emoji_risk": result["emoji_report"]["risk"],
        })

    if results:
        # Save CSV
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"✅ Chat analysis complete! Report saved to {output_path}")

        # Print summary
        summary_text = generate_summary(results)
        print(summary_text)

        # Save summary to file if path provided
        if summary_path:
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary_text)
            print(f"📄 Summary saved to {summary_path}")
        
         # --- NEW: Generate Word report ---
        docx_path = output_path.replace(".csv", ".docx")
        generate_doc_report(results, docx_path)
        print(f"📄 Word report generated: {docx_path}")
        
    return results

def generate_summary(results) -> str:
    total = len(results)
    risk_counts = Counter([r["risk_level"] for r in results])
    sentiments = Counter([r["sentiment"] for r in results])

    all_keywords = []
    for r in results:
        if r["keywords"] != "None":
            all_keywords.extend(r["keywords"].split(", "))
    top_keywords = Counter(all_keywords).most_common(5)

    summary = []
    summary.append("\n📊 Chat Analysis Summary")
    summary.append("-" * 40)
    summary.append(f"Total messages: {total}")
    for level in ["HIGH", "MEDIUM", "LOW"]:
        count = risk_counts.get(level, 0)
        percent = (count / total) * 100 if total else 0
        summary.append(f"{level}: {count} ({percent:.1f}%)")

    if top_keywords:
        summary.append("Top Keywords: " + ", ".join([f"{k} ({v})" for k, v in top_keywords]))
    else:
        summary.append("Top Keywords: None")

    if sentiments:
        dominant = sentiments.most_common(1)[0][0]
        summary.append("Dominant Sentiment: " + dominant)

    return "\n".join(summary)

if __name__ == "__main__":
    chat_file = input("Enter path to chat file: ").strip()
    print("Select platform (whatsapp, telegram, messenger, signal) or press Enter for universal scan:")
    platform = input("Platform: ").strip() or None
    summary_file = input("Enter path to save summary (press Enter to skip): ").strip() or None
    analyze_chat(chat_file, platform=platform, summary_path=summary_file)
