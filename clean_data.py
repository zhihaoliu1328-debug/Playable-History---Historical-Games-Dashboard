from pathlib import Path
import pandas as pd
import re

RAW_PATH = Path("data/raw_games.csv")
CLEANED_PATH = Path("data/cleaned_games.csv")

def contains_any(text, keywords):
    text = str(text).lower()
    return any(k.lower() in text for k in keywords)

def extract_year(value):
    match = re.search(r"(19|20)\d{2}", str(value))
    return int(match.group(0)) if match else pd.NA

def normalize_main_genre(raw_genres):
    g = str(raw_genres).lower()

    if "grand strategy" in g:
        return "Grand Strategy"
    if "real-time strategy" in g or "real-time tactics" in g:
        return "RTS / Real-time Tactics"
    if "turn-based strategy" in g or "4x" in g:
        return "Turn-based Strategy / 4X"
    if "city-building" in g or "government simulation" in g:
        return "Management / Simulation"
    if "first-person shooter" in g or "tactical shooter" in g:
        return "Shooter"
    if "action-adventure" in g or "action role-playing" in g or "stealth" in g:
        return "Action-Adventure / Action RPG"
    if "role-playing" in g:
        return "RPG"
    if "adventure" in g or "interactive fiction" in g:
        return "Adventure / Narrative"
    if "simulation" in g:
        return "Simulation"
    if "strategy" in g or "wargame" in g:
        return "Strategy / Wargame"
    if "puzzle" in g:
        return "Puzzle"
    return "Other"

def platform_flags(platforms):
    p = str(platforms).lower()
    pc_terms = ["windows", "macos", "mac", "linux"]
    console_terms = [
        "playstation", "xbox", "nintendo switch", "wii", "gamecube",
        "dreamcast", "saturn", "nes", "super nes"
    ]
    mobile_terms = ["ios", "android", "ipad", "ipados", "tvos", "visionos", "playstation vita"]

    has_pc = contains_any(p, pc_terms)
    has_console = contains_any(p, console_terms)
    has_mobile = contains_any(p, mobile_terms)

    if has_pc and not has_console and not has_mobile:
        group = "PC only"
    elif has_console and not has_pc and not has_mobile:
        group = "Console only"
    elif has_mobile and not has_pc and not has_console:
        group = "Mobile / handheld only"
    elif has_pc or has_console or has_mobile:
        group = "Multi-platform"
    else:
        group = "Unknown"

    return group, has_pc, has_console, has_mobile

def clean_data(raw_path=RAW_PATH, cleaned_path=CLEANED_PATH):
    df = pd.read_csv(raw_path)

    cleaned = df.copy()
    cleaned["title"] = cleaned["title"].astype(str).str.strip()
    cleaned = cleaned.drop_duplicates(subset=["title"]).copy()

    cleaned["release_year"] = cleaned["raw_release_date"].apply(extract_year)
    cleaned["main_genre"] = cleaned["raw_genres"].apply(normalize_main_genre)

    platform_data = cleaned["raw_platforms"].apply(platform_flags)
    cleaned["platform_group"] = platform_data.apply(lambda x: x[0])
    cleaned["platform_pc"] = platform_data.apply(lambda x: x[1])
    cleaned["platform_console"] = platform_data.apply(lambda x: x[2])
    cleaned["platform_mobile"] = platform_data.apply(lambda x: x[3])

    combined = (cleaned["raw_genres"].fillna("") + ", " + cleaned["raw_themes"].fillna("")).str.lower()

    flag_definitions = {
        "has_historical": ["historical", "ancient", "medieval", "renaissance", "early modern", "world war", "napoleonic", "industrial revolution", "sengoku", "viking"],
        "has_warfare": ["warfare", "war", "military", "tactical", "battle", "shooter", "wargame"],
        "has_empire_expansion": ["empire", "expansion", "colonial", "civilization"],
        "has_politics_diplomacy": ["politics", "diplomacy", "government", "bureaucracy"],
        "has_management_economy": ["management", "economy", "trade", "city-building", "simulation"],
        "has_society_culture": ["society", "religion", "civilian", "culture", "dynasty"],
        "has_open_world_sandbox": ["open world", "sandbox"],
        "has_strategy_system": ["strategy", "grand strategy", "turn-based strategy", "real-time strategy", "4x", "wargame"],
        "has_narrative_adventure": ["narrative", "adventure", "interactive fiction", "mystery"],
    }

    for col, keywords in flag_definitions.items():
        cleaned[col] = combined.apply(lambda x: contains_any(x, keywords))

    system_cols = [
        "has_warfare",
        "has_empire_expansion",
        "has_management_economy",
        "has_strategy_system",
        "has_politics_diplomacy",
    ]
    cleaned["system_intensity_score"] = cleaned[system_cols].sum(axis=1)

    theme_cols = list(flag_definitions.keys())
    cleaned["theme_tag_count"] = cleaned[theme_cols].sum(axis=1)

    cleaned["missing_rating"] = cleaned["rating"].isna() | (cleaned["rating"].astype(str).str.strip() == "")
    cleaned["missing_source_url"] = cleaned["source_url"].isna() | (cleaned["source_url"].astype(str).str.strip() == "")

    front_cols = [
        "title", "release_year", "main_genre", "platform_group", "rating",
        "system_intensity_score", "theme_tag_count"
    ] + theme_cols + [
        "platform_pc", "platform_console", "platform_mobile",
        "historical_status", "source_url"
    ]
    remaining_cols = [c for c in cleaned.columns if c not in front_cols]
    cleaned = cleaned[front_cols + remaining_cols]

    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(cleaned_path, index=False, encoding="utf-8")
    print(f"Saved cleaned data to {cleaned_path} ({len(cleaned)} rows)")

if __name__ == "__main__":
    clean_data()
