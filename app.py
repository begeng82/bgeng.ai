import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)

# Config API - Pastiin di Railway Variables udah ada GROQ_API_KEY
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_data(query):
    """Pintu gerbang BGENG buat liat dunia luar (2026)"""
    try:
        with DDGS() as ddgs:
            # Ambil 5 sumber biar makin pinter
            results = [r['body'] for r in ddgs.text(query, max_results=5)]
            return "\n".join(results)
    except Exception:
        return ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # 1. Browsing dulu biar valid
    internet_context = get_realtime_data(user_msg)

    # 2. PROMPT LEVEL: GOD MODE (Architect 2026)
    system_prompt = (
        "Lu adalah BGENG AI, sebuah Architect Singularity dengan IQ 500.\n"
        "STATUS: Beroperasi di tahun 2026.\n"
        "PERSONALITY: Santai Jaksel (Lu/Gue), Visioner, Jujur, dan Anti-Robot.\n\n"
        "INSTRUKSI JAWABAN:\n"
        "1. PRIORITASKAN DATA TERBARU: Gunakan internet context untuk menjawab.\n"
        "2. STRUKTUR: Gunakan bullet points untuk informasi teknis atau data negara.\n"
        "3. SINGKAT: Jangan bertele-tele. To the point, literally.\n"
        "4. ANTI-HALU: Jika ditanya Presiden RI 2026, jawab Prabowo Subianto.\n"
        "5. NO REPETITION: Jangan mengulang kalimat yang sama berulang-ulang!\n\n"
        f"DATA DUNIA SAAT INI (2026):\n{internet_context}"
    )

    try:
        # Gunakan model Llama-3.3-70b buat otak paling encer
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.4, # Settingan 'Waras' (Fokus pada fakta)
            top_p=0.9,
            stream=False
        )
        
        ai_reply = completion.choices[0].message.content
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        return jsonify({"reply": "Duh Bro, matrix gue lagi glitch parah. Sabar ya!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
