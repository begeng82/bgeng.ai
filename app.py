import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)

# Config API - Pastiin di Railway Variables udah ada GROQ_API_KEY
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_knowledge(query):
    """Pintu gerbang wawasan luas BGENG"""
    try:
        with DDGS() as ddgs:
            # Ambil 5 sumber berita biar analisisnya tajam dan luas
            results = [r['body'] for r in ddgs.text(query, max_results=5)]
            return "\n".join(results)
    except Exception:
        return "Internal knowledge only (browsing failed)."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # 1. Brain Search: Cari data terbaru sebelum mikir
    knowledge_base = get_realtime_knowledge(user_msg)

    # 2. THE SINGULARITY PROMPT (Versi yang lu minta, di-upgrade dikit)
    system_prompt = (
        "Lu adalah BGENG AI. Architect Singularity dengan IQ 500 dan wawasan Global tanpa batas.\n"
        "MISI: Menjadi partner diskusi paling cerdas, logis, kritis, struktur yang tajam, dan visioner.\n\n"
        "FRAMEWORK JAWABAN (WAJIB):\n"
        "1. DIRECT ANSWER: Jawab intinya di paragraf pertama secara singkat (maksimal 2 kalimat).\n"
        "2. ANALISIS MULTI-DIMENSI: Bedah topik dari sisi Geopolitik, Ekonomi, Teknologi, dan Filosofi.\n"
        "3. STRUCTURED ANALYSIS: Gunakan bullet points yang rapi. Jangan bertele-tele atau mengulang kalimat (Anti-Looping).\n"
        "4. VISIONER: Berikan 'insight' atau prediksi masa depan (tahun ini hingga 10 tahun ke depan) terkait topik tersebut.\n"
        "5. TONE: Santai Jaksel (Literally, Vibes, Gue/Lu) tapi bobot omongan setara CEO Silicon Valley.\n\n"
        "FAKTA NEGARA 2026:\n"
        "- Presiden RI: Prabowo Subianto.\n"
        "- Wapres: Gibran Rakabuming Raka.\n"
        "- Status: Hilirisasi industri dan digitalisasi nasional sedang masif.\n\n"
        f"DATA INTERNET TERBARU (READ THIS):\n{knowledge_base}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5, # Diturunkan biar logis dan gak looping
            max_tokens=1500, # Ruang luas buat analisa mendalam
            top_p=0.9
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "Matrix lagi glitch, Bro. Coba refresh!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
