from flask import Flask, request, jsonify
from flask_cors import CORS
from kanana_nano_model.kanana import generate_answer, load_model

app = Flask(__name__)
CORS(app)

# 서버 시작 시 모델 미리 로딩
print("서버 시작 중... 모델을 로딩합니다.")
load_model()
print("서버가 준비되었습니다!")

@app.route('/')
def home():
    return "Hello, this is a simple Python server!"

@app.route('/chat', methods=['POST'])
def chat():

    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No message  provided'}), 400
    
    response = generate_answer(user_input)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 