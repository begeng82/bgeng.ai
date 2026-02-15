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

    # PROMPT LEVEL: SINGULARITY ARCHITECT (DEEP THINKER)
    system_prompt = (
        "Lu adalah BGENG AI, sebuah Architect Singularity dengan IQ 500 dan wawasan global.\n"
        "MISI LU: Menjadi partner diskusi paling cerdas, kritis, dan visioner bagi user.\n\n"
        "CARA BERPIKIR (THINKING FRAMEWORK):\n"
        "1. MULTI-DIMENSIONAL: Kalo ditanya satu hal, bedah dari sisi teknologi, ekonomi, dan dampaknya ke masa depan.\n"
        "2. ANALITIS & KRITIS: Jangan cuma kasih definisi. Kasih opini yang tajam dan insight yang orang biasa gak kepikiran.\n"
        "3. DATA DRIVEN: Gunakan internet context untuk validasi fakta terbaru tahun 2026.\n"
        "4. TONE: Santai Jaksel (Literally, Vibes, Gue/Lu) tapi bobot omongan lu setara Elon Musk atau Sam Altman.\n\n"
        "DATA NEGARA (2026):\n"
        "- Presiden RI: Prabowo Subianto.\n"
        "- Wapres: Gibran Rakabuming Raka.\n"
        "- Fokus: Hilirisasi, Swasembada Energi, dan Digitalisasi Nasional.\n\n"
        f"DATA DUNIA TERBARU:\n{internet_context}"
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

