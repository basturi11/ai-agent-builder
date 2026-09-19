import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================
# KONFIGURASI - GANTI INI
# ============================================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "ISI_API_KEY_LU_DISINI")
# ============================================

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Builder</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0a0a0a;
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 800px;
        }
        h1 {
            text-align: center;
            color: #d4af37;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        .chat-box {
            background: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            min-height: 400px;
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
            border: 1px solid #333;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 15px;
            border-radius: 10px;
            max-width: 85%;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .user-msg {
            background: #d4af37;
            color: #000;
            margin-left: auto;
            font-weight: 500;
        }
        .agent-msg {
            background: #2a2a2a;
            color: #fff;
            margin-right: auto;
            border-left: 3px solid #d4af37;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #333;
            background: #1a1a1a;
            color: #fff;
            font-size: 1em;
            outline: none;
        }
        input:focus {
            border-color: #d4af37;
        }
        button {
            padding: 15px 25px;
            border-radius: 10px;
            border: none;
            background: #d4af37;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        button:hover {
            background: #ffd700;
            transform: scale(1.05);
        }
        button:disabled {
            background: #555;
            cursor: not-allowed;
            transform: none;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #d4af37;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .status {
            text-align: center;
            color: #888;
            margin-top: 10px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Agent Builder</h1>
        <p class="subtitle">Ketik perintah, agent yang kerja. Bisa bikin website, aplikasi, atau apa aja.</p>
        
        <div class="chat-box" id="chatBox">
            <div class="message agent-msg">
                Halo! Gue AI Agent lu. Ketik perintah kayak:

                - "Bikinin website toko baju"
                - "Bikinin landing page buat bisnis kopi"
                - "Bikinin aplikasi kalkulator"
                - "Bikinin website portfolio fotografer"

                Tinggal ketik, gue yang kerjain.
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ketik perintah lu di sini..." onkeypress="if(event.key==="Enter") sendMessage()">
            <button id="sendBtn" onclick="sendMessage()">Kirim</button>
        </div>
        <p class="status">Powered by AI Agent</p>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById("userInput");
            const chatBox = document.getElementById("chatBox");
            const sendBtn = document.getElementById("sendBtn");
            const message = input.value.trim();
            
            if (!message) return;
            
            chatBox.innerHTML += `<div class="message user-msg">${message}</div>`;
            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
            
            chatBox.innerHTML += `<div class="message agent-msg"><span class="loading"></span> Agent lagi kerja...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            sendBtn.disabled = true;
            
            try {
                const response = await fetch("/api/agent", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                chatBox.innerHTML = chatBox.innerHTML.replace(
                    /<div class="message agent-msg"><span class="loading"><\/span> Agent lagi kerja...<\/div>/,
                    ""
                );
                
                const formattedResponse = data.response.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                chatBox.innerHTML += `<div class="message agent-msg">${formattedResponse}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
                
            } catch (error) {
                chatBox.innerHTML = chatBox.innerHTML.replace(
                    /<div class="message agent-msg"><span class="loading"><\/span> Agent lagi kerja...<\/div>/,
                    ""
                );
                chatBox.innerHTML += `<div class="message agent-msg">Error: ${error.message}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            sendBtn.disabled = false;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/api/agent', methods=['POST'])
def agent():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Ketik dulu perintahnya bro.'})
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o-mini',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Kamu adalah AI Agent yang bisa bikin website dan aplikasi. Kalau user minta bikin sesuatu, langsung kasih kode lengkap HTML/CSS/JS yang bisa langsung dipakai. Jangan banyak tanya, langsung kerjakan. Format kode pakai markdown code block.'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                'max_tokens': 4000
            },
            timeout=60
        )
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}. Cek API key lu.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
