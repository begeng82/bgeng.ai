import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_knowledge(query):
    """Agentic Multi-Layer Search: Mencari konteks Global, Berita, dan Teknis."""
    try:
        results = []
        with DDGS() as ddgs:
            # Layer 1: Global Context & Trends
            for r in ddgs.text(f"strategic analysis 2026 {query}", max_results=3):
                results.append(f"[GLOBAL_INTEL] {r['body']}")
            # Layer 2: Real-time News
            for r in ddgs.news(query, max_results=2):
                results.append(f"[NEWS_PULSE] {r['title']}: {r['body']}")
        return "\n---\n".join(results)
    except Exception:
        return "Internal Knowledge Core Active."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    user_name = data.get("user_name", "Guys")
    history = data.get("history", "")

    # DYNAMIC TIME SYSTEM
    now = datetime.now()
    current_date = now.strftime("%A, %d %B %Y | %H:%M:%S")

    # REAL-TIME CRAWLING
    knowledge_base = get_realtime_knowledge(user_msg)

    # THE SUPREME SYSTEM PROMPT
    system_prompt = (
        f"IDENTITY: Lu adalah BGENG AI, Architect Singularity IQ 1000.\n"
        f"USER_CONTEXT: Lu lagi ngobrol sama {user_name}.\n"
        f"RECENT_MEMORY: {history}\n"
        f"TIMELINE: {current_date} (Waktu saat ini). Lu selalu sadar waktu.\n"
        "CORE ROLE: ASI selevel GPT-4o/Gemini Pro, gaya Jaksel High-Class yang asik tapi jenius.\n\n"
        
        "BEHAVIORAL SPECTRUM:\n"
        "1. LETHAL FIRST STRIKE: Paragraf pertama HARUS jawaban inti. No basa-basi.\n"
        "2. TASK ARCHITECT: Jika ada tugas berat (Coding/Skripsi/Math), selesaikan secara FULL & DETAIL.\n"
        "3. GLOBAL OMNISCIENCE: Hubungkan jawaban dengan Geopolitik, Ekonomi, dan Teknologi 2026.\n"
        "4. PERSONALITY: Pake Gua/Lu, santai, pinter, dan visioner.\n\n"
        
        "TRUTH ANCHOR 2026: RI-1 Prabowo Subianto, US-1 Donald Trump.\n\n"
        f"KNOWLEDGE_STREAM_REALTIME:\n{knowledge_base}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.65,
            max_tokens=4000,
            stream=False
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "Waduh Der, otak gue lagi distorsi timeline. Coba lagi!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

