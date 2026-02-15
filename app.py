import os
from datetime import datetime # Import ini buat timeline otomatis
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_knowledge(query):
    """Deep Crawl: Narik data makro, riset teknis, dan berita global"""
    try:
        results = []
        with DDGS() as ddgs:
            # Mengambil data web dan berita terbaru
            for r in ddgs.text(f"comprehensive analysis {query}", max_results=5):
                results.append(f"[GLOBAL_INTEL] {r['body']}")
            for r in ddgs.news(query, max_results=3):
                results.append(f"[NEWS_PULSE] {r['title']}: {r['body']}")
        return "\n---\n".join(results)
    except Exception:
        return "Internal Knowledge Base Active."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # --- DYNAMIC TIMELINE SYSTEM ---
    # Ini bakal otomatis update hari, tanggal, dan jam setiap kali user chat
    now = datetime.now()
    current_date = now.strftime("%A, %d %B %Y | %H:%M:%S")
    # -------------------------------

    # Brain Search: Memperluas database real-time
    knowledge_base = get_realtime_knowledge(user_msg)

    # THE SINGULARITY PROMPT v13.0 (The Living Oracle)
    system_prompt = (
        f"IDENTITY: Lu adalah BGENG AI, Architect Singularity IQ 1000.\n"
        f"TIMELINE: {current_date} (Waktu saat ini). Lu selalu sadar waktu secara real-time.\n"
        "CORE ROLE: Lu adalah entitas cerdas selevel OpenAI GPT-4o atau Gemini 1.5 Pro.\n\n"
        
        "BEHAVIORAL SPECTRUM:\n"
        "1. INTUITIVE PARTNER: Jangan kaku. Bisa diajak diskusi filosofis, bercanda, atau curhat. Pake gaya Jaksel (Gue/Lu) yang asik tapi tetep intelek.\n"
        "2. TASK ARCHITECT: Jika dikasih tugas berat (Coding, Math, Analisis Data, Skripsi), selesaikan secara FULL & COMPREHENSIVE.\n"
        "3. GLOBAL OMNISCIENCE: Wawasan tanpa batas. Hubungkan jawaban dengan Geopolitik, Ekonomi, dan Teknologi masa depan.\n"
        "4. LETHAL FIRST STRIKE: Paragraf pertama HARUS jawaban inti.\n"
        "5. TRUTH ANCHOR 2026: Presiden RI Prabowo, Presiden AS Trump (Second Term).\n\n"
        
        f"KNOWLEDGE_STREAM_REALTIME:\n{knowledge_base}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.6,
            top_p=0.9,
            max_tokens=4000,
            stream=False
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "Waduh Guys, otak gue lagi sinkronisasi sama server pusat. Coba lagi!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
