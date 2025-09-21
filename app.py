from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import zai
from zai import ZhipuAiClient

app = Flask(__name__)
CORS(app)

# 初始化智谱AI客户端
client = ZhipuAiClient(api_key="ce6f2a1356ef4716a151749b62eb8ab8.SzkhEvNbJ4ZjSha4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        temperature = data.get('temperature', 0.6)
        
        response = client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个有用的AI助手。"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=temperature
        )
        
        ai_response = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 使用 0.0.0.0 让服务器监听所有网络接口
    app.run(host='0.0.0.0', port=5000, debug=True)