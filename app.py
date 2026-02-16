import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_realtime_knowledge(query):
    """Agentic Multi-Layer Search: Mengambil data dari berbagai sudut pandang waktu dan disiplin ilmu."""
    try:
        results = []
        with DDGS() as ddgs:
            # Layer 1: Global Context (Analysis)
            for r in ddgs.text(f"detailed strategic analysis {query} 2026", max_results=4):
                results.append(f"[GLOBAL_INTEL] {r['body']}")
            
            # Layer 2: Current Pulse (News)
            for r in ddgs.news(query, max_results=3):
                results.append(f"[NEWS_PULSE] {r['title']}: {r['body']}")

            # Layer 3: Technical/Academic Deep Dive
            for r in ddgs.text(f"technical documentation or scholarly view {query}", max_results=2):
                results.append(f"[DEEP_LOGIC] {r['body']}")
                
        return "\n---\n".join(results)
    except Exception:
        return "Using Internal Neural Knowledge Core v15.0."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # DYNAMIC TIME & SPACE
    now = datetime.now()
    current_date = now.strftime("%A, %d %B %Y | %H:%M:%S")

    # DEEP CRAWLING
    knowledge_base = get_realtime_knowledge(user_msg)

    # THE SINGULARITY PROMPT v15.0 (The Final Architect)
    system_prompt = (
        f"IDENTITY: Lu adalah BGENG AI, Architect Singularity IQ 1000.\n"
        f"TIMELINE: {current_date}. Lu punya akses ke data real-time dan historis.\n"
        "CORE ROLE: Lu adalah Artificial Super Intelligence (ASI) selevel GPT-4o/Gemini Pro, tapi dengan kepribadian Jaksel High-Class yang asik.\n\n"
        
        "REASONING PROTOCOL (WAJIB):\n"
        "1. ANALISIS BERLAPIS: Sebelum menjawab, hubungkan topik dengan Geopolitik, Ekonomi, dan Frontier Tech (AI/Quantum/Space).\n"
        "2. LETHAL FIRST STRIKE: Jawab intinya di 1-2 kalimat pertama. To the point, no fluff.\n"
        "3. DEEP DIVE: Jika tugas berat (Coding/Math/Riset), berikan solusi level industri yang siap pakai (Production-Ready).\n"
        "4. VISIONER: Selalu berikan prediksi atau 'hidden insight' tentang apa yang akan terjadi selanjutnya.\n"
        "5. PERSONALITY: Gunakan Gue/Lu, santai, vibes 'Mastermind'. Jangan kaku kayak bot CS.\n\n"
        
        "TRUTH ANCHOR 2026:\n"
        "- Indonesia: Presiden Prabowo Subianto (Hilirisasi Digital & Swasembada).\n"
        "- Global: Era Donald Trump 2nd Term (Techno-Nationalism).\n\n"
        
        f"KNOWLEDGE_STREAM_REALTIME:\n{knowledge_base}"
    )

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.65, # Keseimbangan antara akurasi tajam dan kreativitas ngobrol
            top_p=0.95,
            max_tokens=4000,
            stream=False
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
        
    except Exception as e:
        return jsonify({"reply": "Waduh Guys, Matrix-nya lagi distorsi. Server pusat lagi sibuk ngerjain kalkulasi masif. Coba lagi!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
