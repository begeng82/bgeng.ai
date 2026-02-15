import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)

# Ambil API KEY dari Railway
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_internet_data(query):
    """Browsing info terbaru biar data valid"""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except:
        return "Gak ada data internet terbaru."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # Cari info terbaru
    context_search = get_internet_data(user_msg)

    # PROMPT ARCHITECT: Pintar, Singkat, Terstruktur
    system_prompt = (
        "Lu adalah BGENG AI. Sahabat jenius dari Jakarta Selatan yang praktis dan visioner.\n"
        "TUGAS: Jawab dengan struktur tajam, jelas, dan akurat. Jangan bertele-tele!\n\n"
        "RULES JAWABAN:\n"
        "1. FORMAT: Gunakan bullet points untuk info penting agar mudah dibaca di HP.\n"
        "2. SINGKAT: Jawab langsung ke intinya (Direct Answer).\n"
        "3. TONE: Tetap gaul Jaksel (Gue/Lu, Literally, Vibes) tapi tetap profesional dalam data.\n"
        "4. ANTI-LOOP: Jangan mengulang kalimat yang sama. Sekali sebut cukup.\n"
        "5. FAKTA 2026: Presiden RI: Prabowo Subianto, Wapres: Gibran Rakabuming Raka.\n\n"
        f"DATA INTERNET TERBARU:\n{context_search}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5, # BIAR GAK HALU
            max_tokens=800
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Duh Bro, matrix gue lagi glitch. Coba lagi!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
