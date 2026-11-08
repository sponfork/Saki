import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_hero_database():
    with open("mlbb_heroes_clean.json", "r", encoding="utf-8") as f:
        return json.load(f)

def query_ai_with_rag(user_prompt):
    heroes = load_hero_database()
    
    target_hero = None
    for hero in heroes:
        if hero["name"].lower() in user_prompt.lower():
            target_hero = hero
            break

    if target_hero:
        context_data = json.dumps(target_hero, indent=2)
        print(f"\n[+] RAG Retrieval: Loaded counter matchup data for {target_hero['name']}")
    else:
        context_data = json.dumps(heroes[:20], indent=2)
        print(f"\n[+] RAG Retrieval: Loaded general hero database sample")

    full_prompt = f"""
    You are an expert Mobile Legends: Bang Bang (MLBB) draft assistant.
    
    STATISTICAL DATA CONTEXT:
    {context_data}
    
    User Query: {user_prompt}
    Provide precise, tactical draft advice based strictly on the provided counter scores and dataset.
    """

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": full_prompt}]
    )
    
    return response.choices[0].message.content

def main():
    print("==================================================")
    print("   MLBB RAG Draft Assistant (Active & Ready)     ")
    print("==================================================")
    print("Type an enemy hero to get counters, or type 'exit' to quit.\n")
    
    while True:
        user_input = input("Draft Query > ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Good luck in your matches!")
            break
        
        if not user_input:
            continue
            
        try:
            answer = query_ai_with_rag(user_input)
            print(f"\nAssistant:\n{answer}\n" + "-"*50)
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()