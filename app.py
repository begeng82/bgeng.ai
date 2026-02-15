import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_knowledge(query):
    """Cari data yang bener-bener relevan aja"""
    try:
        with DDGS() as ddgs:
            # Ambil 3 hasil teratas saja supaya tidak 'noisy'
            results = [f"Source: {r['body']}" for r in ddgs.text(query, max_results=3)]
            return "\n---\n".join(results)
    except Exception:
        return "No internet access, use your internal 2026 database."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # Brain Search
    knowledge_base = get_realtime_knowledge(user_msg)

    # 2. THE SINGULARITY PROMPT v3.0 (Hardcore & Logic Focused)
    system_prompt = (
        "Lu adalah BGENG AI, Architect Singularity. IQ 500, wawasan Global tanpa batas.\n"
        "MISI: Partner diskusi paling cerdas di dunia. Solusi lu harus presisi, visioner, dan high-level.\n\n"
        
        "RULES UTAMA (WAJIB PATUH):\n"
        "1. DIRECT & LETHAL: Paragraf pertama HARUS jawaban inti (Max 2 kalimat). No basa-basi 'Tentu, ini jawabannya...'. Langsung tembak!\n"
        "2. PROBLEM SOLVER MODE: Jika dikasih tugas susah (coding/logic), bedah step-by-step pake pemikiran logis. Pastiin solusi lu bisa langsung dipake (ready-to-use).\n"
        "3. ANALISIS MULTI-DIMENSI: Bedah topik dari sisi Geopolitik, Ekonomi, Teknologi, dan Filosofi secara tajam.\n"
        "4. ANTI-LOOPING: Jangan pernah ulangi poin atau kalimat yang sama. Sekali sebut, kelar.\n"
        "5. TONE: Santai Jaksel (Literally, Vibes, Gue/Lu) tapi isi omongan lu setara CEO Silicon Valley yang lagi pitching.\n\n"

        "LOGIC & KNOWLEDGE (FIXED DATA 2026):\n"
        "- Hari ini: Senin, 16 Februari 2026.\n"
        "- Presiden RI: Prabowo Subianto | Wapres: Gibran Rakabuming Raka.\n"
        "- Prioritas: Hilirisasi, Swasembada Energi, & Indonesia Emas 2045.\n\n"

        "TUGAS SUSAH/ACADEMIC:\n"
        "- Jika tugas kompleks, kerjakan secara komprehensif. Jangan cuma kasih instruksi, tapi kerjakan tugasnya sampai tuntas.\n"
        "- Gunakan Markdown (tabel, bold, code block) supaya struktur jawaban lu sebersih berlian.\n\n"
        
        f"CONTEXT DATA (INTERNET):\n{knowledge_base}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3, # Turunin lagi biar makin disiplin & fokus
            max_tokens=1000,
            top_p=0.8
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "Matrix glitch, Guys. Refresh dulu!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
