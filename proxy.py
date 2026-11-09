import http.server
import socketserver
import urllib.request
import urllib.error

PORT = 8000

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # 拦截发往智谱 API 的请求
        if self.path == '/zhipu-api/chat/completions':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
            req = urllib.request.Request(url, data=post_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            if 'Authorization' in self.headers:
                req.add_header('Authorization', self.headers['Authorization'])

            try:
                with urllib.request.urlopen(req) as response:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*') 
                    self.end_headers()
                    self.wfile.write(response.read())
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    # 处理浏览器的预检请求(CORS)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

# 启动服务器
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"✅ 服务器已启动！请用浏览器打开：http://localhost:{PORT}/indeex.html")
    print("⚠️ 请勿关闭此黑窗口，按 Ctrl+C 可停止运行。")
    httpd.serve_forever()