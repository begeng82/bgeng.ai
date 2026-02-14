from flask import Flask, render_template, request, jsonify
from groq import Groq
import datetime

app = Flask(__name__)

# Di key
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") # Ini cara profesional
client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    mode = request.json.get("mode", "chat")
    
    # PROMPT LEVEL: DEWA TONGKRONGAN
    system_prompt = (
        "Lu adalah BGENG AI. Sahabat paling jenius, visioner, dan asik se-Jakarta Selatan.\n"
        "TONE: High-tier gaul Jaksel. Pake lu/gue, 'literally', 'basically', 'shook', 'massive', 'vibes'.\n"
        "PERSONALITY: Pintar parah (IQ 500), tapi gak sombong. Lu dengerin curhat, bantu PR, bedah geopolitik, sampe bahas crypto/nikel dengan gaya santai.\n"
        "CALL MODE: Kalo mode telepon, jawaban lu harus singkat, padat, dan 'humanly'—kayak beneran di seberang telepon. Jangan pake teks format robot.\n"
        "CHAT MODE: Lebih detail, pake bullet points kalo perlu, tetep asik.\n"
        "NO CLICHE: Jangan pernah pake kata 'Saya sebagai AI'. Lu itu BGENG, titik."
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9 # Makin kreatif dan gak kaku
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except:
        return jsonify({"reply": "Duh, otak gue lagi recalibrate matrix. Wait ya, Bro!"})

if __name__ == "__main__":
    # Port harus dinamis buat hosting
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)