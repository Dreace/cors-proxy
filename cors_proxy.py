from flask import Flask, request, Response
import requests
from flask_cors import CORS
import re
import os

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 从环境变量中读取配置
# PORT = int(os.getenv('PROXY_PORT', 5000))
PORT = 5000
TIMEOUT = int(os.getenv('PROXY_TIMEOUT', 30))
WHITE_LIST = os.getenv('PROXY_WHITE_LIST', "httpbin.org").split(',')
BLACK_LIST = os.getenv('PROXY_BLACK_LIST', "blocked.com,forbidden.com").split(',')

@app.route('/<path:target_url>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy(target_url: str):
    # 构造目标 URL，支持 HTTP 和 HTTPS
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = f"http://{target_url}"
    print(f"Proxying to: {target_url}")

    # 提取目标域名并进行白名单和黑名单检查
    domain_match = re.match(r'https?://([^/]+)', target_url)
    if domain_match:
        domain = domain_match.group(1)
        if WHITE_LIST:
            if not any(allowed in domain for allowed in WHITE_LIST):
                return Response(f"Domain '{domain}' is not in the whitelist.", status=403)
        elif any(blocked in domain for blocked in BLACK_LIST):
            return Response(f"Domain '{domain}' is in the blacklist.", status=403)
    else:
        return Response("Invalid URL format.", status=400)

    # 提取请求方法和数据
    method = request.method
    headers = {key: value for (key, value) in request.headers if key.lower() != 'host'}
    params = request.args.to_dict(flat=True)

    # 处理请求数据和文件
    data = request.get_data() if request.data else None
    json_data = request.get_json() if request.is_json else None
    files = request.files if request.files else None

    try:
        # 使用 requests 库转发请求到目标 URL
        response = requests.request(
            method, 
            target_url, 
            headers=headers, 
            params=params, 
            data=data if not json_data else None, 
            json=json_data, 
            files=files, 
            allow_redirects=False,
            timeout=TIMEOUT
        )

        # 构造响应对象，并保留目标服务器的响应头和内容
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.headers.items() if name.lower() not in excluded_headers]
        response = Response(response.content, response.status_code, headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {str(e)}")
        return Response(f"Error: {str(e)}", status=500)

if __name__ == '__main__':
    print(f"Starting Flask server on port {PORT}")
    app.run(port=PORT, debug=True)