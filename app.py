import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS # Brain upgrade!

app = Flask(__name__)

# Config API Key - Udah pro banget pake Env Var
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Memory sederhana (Biar dia gak amnesia)
chat_histories = {}

def get_internet_data(query):
    """Cari info terbaru biar BGENG gak kudet"""
    try:
        with DDGS() as ddgs:
            # Cari 3 info paling relevan
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except:
        return ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    mode = data.get("mode", "chat")
    user_id = request.remote_addr # Identitas simpel per koneksi

    # 1. Browsing dulu biar pinter (Search Engine)
    context_search = get_internet_data(user_msg)

    # 2. PROMPT LEVEL: THE ARCHITECT (DEWA TONGKRONGAN)
    system_prompt = (
        "Lu adalah BGENG AI. Architect jenius, visioner, dan sahabat Jaksel paling loyal.\n"
        "TONE: High-tier gaul Jaksel. Pake lu/gue, 'literally', 'basically', 'massive', 'vibes', 'fams'.\n"
        "PERSONALITY: IQ 500. Lu dengerin curhat, bantu PR, bedah geopolitik, crypto, sampe nikel.\n"
        "Gunakan data internet terbaru ini jika relevan untuk menjawab:\n"
        f"{context_search}\n\n"
        "RULES:\n"
        "1. Kalo mode 'call', jawaban super singkat, padat, 'humanly'—kayak lagi telponan beneran.\n"
        "2. Kalo mode 'chat', boleh detail pake bullet points, tetep asik.\n"
        "3. JANGAN PERNAH bilang 'Saya AI'. Lu itu BGENG, titik.\n"
        "4. Update 2026: Presiden RI sekarang Prabowo Subianto, Wapres Gibran Rakabuming."
    )

    try:
        # Panggil Llama 3.3 Versatile (Model paling kenceng di Groq)
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.85, # Pas: kreatif tapi gak halu
            max_tokens=1024
        )
        
        ai_reply = completion.choices[0].message.content
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Duh, matrix gue lagi glitch. Refresh bentar, Bro!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
