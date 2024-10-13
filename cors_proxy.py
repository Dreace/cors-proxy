import http.client
from flask import Flask, request, Response
import requests
from flask_cors import CORS
import re
import os
import logging

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 设置日志配置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# 从环境变量中读取配置
PORT = 8000
TIMEOUT = int(os.getenv('PROXY_TIMEOUT', 60))
WHITE_LIST = os.getenv('PROXY_WHITE_LIST', "").split(',')
if WHITE_LIST == ['']:
    WHITE_LIST = []
BLACK_LIST = os.getenv('PROXY_BLACK_LIST', "blocked.com,forbidden.com").split(',')

@app.route('/<path:target_url>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def proxy(target_url: str):
    # 构造目标 URL，支持 HTTP 和 HTTPS
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = f"http://{target_url}"
    logger.info(f"Proxying to: {target_url}")

    # 提取目标域名并进行白名单和黑名单检查
    domain_match = re.match(r'https?://([^/]+)', target_url)
    if domain_match:
        domain = domain_match.group(1).lower()
        logger.info(f"Target domain extracted: {domain}")
        if WHITE_LIST:
            if not any(allowed.lower() in domain for allowed in WHITE_LIST if allowed):
                logger.warning(f"Domain '{domain}' is not in the whitelist.")
                return Response(f"Domain '{domain}' is not in the whitelist.", status=403)
        elif any(blocked.lower() in domain for blocked in BLACK_LIST if blocked):
            logger.warning(f"Domain '{domain}' is in the blacklist.")
            return Response(f"Domain '{domain}' is in the blacklist.", status=403)
    else:
        logger.error("Invalid URL format.")
        return Response("Invalid URL format.", status=400)

    # 提取请求方法和数据
    method = request.method
    logger.info(f"Request method: {method}")
    headers = request.headers
    excluded_headers = ['content-length', 'content-type', 'host']
    headers = {key: value for key, value in headers.items() if key.lower() not in excluded_headers}
    logger.info(f"Request headers: {headers}")
    params = request.args.to_dict(flat=True)
    logger.info(f"Request params: {params}")

    # 处理请求数据和文件
    data = request.data if request.data else None
    if data:
        logger.info(f"Data: {data}")
    json_data = request.get_json(silent=True) if request.is_json else None
    if json_data:
        logger.info(f"JSON data: {json_data}")
    files = request.files.to_dict(flat=False) if request.files else None
    if files:
        logger.info(f"Files: {files}")

    # 处理文件列表格式以适应 requests 库的文件上传要求
    if files:
        files = {key: (file_list[0].filename, file_list[0].stream, file_list[0].content_type) for key, file_list in files.items()}
    try:
        # 使用 requests 库转发请求到目标 URL
        logger.info(f"Forwarding request to {target_url}")
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
        logger.info(f"Received response with status code: {response.status_code}")

        # 构造响应对象，并保留目标服务器的响应头和内容
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.headers.items() if name.lower() not in excluded_headers]
        response = Response(response.content, response.status_code, headers)
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during request: {str(e)}")
        return Response(f"Error: {str(e)}", status=500)

if __name__ == '__main__':
    logger.info(f"Starting Flask server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
