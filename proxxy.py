import os
from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求，解决手机访问拦截

ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

@app.route('/zhipu-api/chat/completions', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        return Response(status=200)
    headers = {
        'Authorization': request.headers.get('Authorization'),
        'Content-Type': 'application/json'
    }
    response = requests.post(ZHIPU_API_URL, headers=headers, json=request.get_json())
    return Response(response.content, status=response.status_code)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)