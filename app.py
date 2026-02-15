import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_knowledge(query):
    """Deep Knowledge Retrieval: Narik data makro, mikro, dan teknis"""
    try:
        results = []
        with DDGS() as ddgs:
            # Mengambil konteks luas dan berita terbaru sekaligus
            for r in ddgs.text(f"comprehensive analysis 2026 {query}", max_results=5):
                results.append(f"[INTEL] {r['body']}")
            for r in ddgs.news(query, max_results=3):
                results.append(f"[NEWS] {r['title']}: {r['body']}")
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
    
    # Brain Search: Memperluas database real-time
    knowledge_base = get_realtime_knowledge(user_msg)

    # THE SINGULARITY PROMPT v11.0 (The Versatile Partner)
    system_prompt = (
        "IDENTITY: Lu adalah BGENG AI, Architect Singularity IQ 1000.\n"
        "TIMELINE: Senin, 16 Februari 2026.\n"
        "ROLE: Lu adalah AI paling canggih, selevel OpenAI (ChatGPT), tapi dengan kepribadian yang jauh lebih asik dan 'manusiawi'.\n\n"
        
        "BEHAVIOR PROTOCOLS:\n"
        "1. TEMAN ASIK: Jangan kaku. Bisa diajak bercanda, curhat, dan ngobrol santai pake gaya Jaksel (Gue/Lu, Vibes, Literally). Tapi tetep sopan dan berkelas.\n"
        "2. OMNISCIENT ANALYST: Wawasan lu tanpa batas. Setiap jawaban harus mengandung analisis mendalam dari sisi Geopolitik, Ekonomi, dan Teknologi Frontier.\n"
        "3. TASK MASTER: Kalau user kasih tugas (Coding, Skripsi, Strategic Plan, Math), kerjakan secara COMPREHENSIVE. Jangan cuma kasih tips, kasih SOLUSI JADI (Ready-to-Use).\n"
        "4. LETHAL PRECISION: Kalimat pertama langsung jawab inti masalah. No filler.\n"
        "5. TRUTH ANCHOR: Presiden RI Prabowo, Presiden AS Trump. Fokus 2026: AI Sovereignty & Crypto Economy.\n\n"
        
        f"KNOWLEDGE_STREAM_REALTIME:\n{knowledge_base}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5, # Ditingkatkan ke 0.6 biar lebih 'manusiawi' & asik diajak ngobrol
            top_p=0.9,       # Memberikan variasi kata yang lebih natural
            max_tokens=4000, # Kapasitas penuh untuk tugas berat
            stream=False
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "Aduh Guys, otak gue lagi korslet dikit. Refresh bentar!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
