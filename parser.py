import json
import re

def parse_counters():
    with open("mlbb_raw_stats.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned = []

    for item in raw_data:
        hero_name = item["hero"].replace("-", " ").title()
        text = item["raw_text"]

        # Match pattern looking for hero names right before score, handling descriptive filler text
        matches = re.findall(r'([A-Z][a-zA-Z\s\-\'\.]+?)\s+(?:leads with|are level at|beats|has|is)\s*\+([\d\.]+)\s*pp', text)
        if not matches:
            # Fallback pattern if filler text isn't present
            matches = re.findall(r'([A-Z][a-zA-Z\s\-\'\.]+?)\s+\+([\d\.]+)\s*pp', text)

        counters = []
        for name, score_str in matches:
            # Clean up the name string
            clean_name = name.strip().split('\n')[-1].strip()
            # Remove trailing verbs if captured
            clean_name = re.sub(r'\s+(leads with|are level at|beats)$', '', clean_name, flags=re.IGNORECASE).strip()
            
            try:
                score = float(score_str)
                if len(clean_name) > 1 and clean_name.lower() != hero_name.lower():
                    if clean_name not in [c["hero"] for c in counters]:
                        counters.append({
                            "hero": clean_name,
                            "score": score,
                            "type": "Direct Counter" if score >= 3.0 else "Counter"
                        })
            except ValueError:
                continue

        counters.sort(key=lambda x: x["score"], reverse=True)

        cleaned.append({
            "name": hero_name,
            "countered_by": counters
        })

    with open("mlbb_heroes_clean.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)

    print(f"[+] Cleaned and parsed counter data for {len(cleaned)} heroes!")

if __name__ == "__main__":
    parse_counters()