from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import json, argparse, os
from .core import ROOT, load, grade, record_review
from .calibration import calibrate
def public_demo():
    return bool(os.getenv('PORT') or os.getenv('TEACHERLENS_PUBLIC_DEMO') == '1')

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        super().end_headers()
    def send_json(self,obj,status=200):
        body=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/healthz': return self.send_json({'status':'ok'})
        if self.path=='/api/config': return self.send_json({'public_demo':public_demo(),'llm_available':not public_demo() and bool(os.getenv('TEACHERLENS_API_KEY') or os.getenv('DASHSCOPE_API_KEY'))})
        if self.path=='/api/demo': return self.send_json(load(ROOT/'data/demo.json'))
        return super().do_GET()
    def do_POST(self):
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n>1_000_000: return self.send_json({'error':'请求过大'},413)
            d=json.loads(self.rfile.read(n))
            if self.path=='/api/calibrate':
                demo=load(ROOT/'data/demo.json')
                return self.send_json(calibrate(demo['rubric'],d['decisions'],d['task_id']))
            if self.path=='/api/grade':
                if public_demo() and d.get('engine','demo') != 'demo': return self.send_json({'error':'公开演示仅支持离线规则引擎'},403)
                if len(d.get('answers',[]))>100: return self.send_json({'error':'每次最多处理100份作答'},400)
                rows=[grade(d['task'],a,d['rubric'],d.get('mode','calibrated'),d.get('engine','demo')) for a in d['answers']]; return self.send_json(rows)
            if self.path=='/api/review': return self.send_json(record_review(d['result'],d['score'],d['reason'],d['scope']))
            return self.send_json({'error':'not found'},404)
        except Exception as e: return self.send_json({'error':'请求处理失败，请检查输入。' if public_demo() else str(e)},400)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--port',type=int,default=int(os.getenv('PORT','8765'))); p.add_argument('--host',default='0.0.0.0' if os.getenv('PORT') else '127.0.0.1'); a=p.parse_args(); server=ThreadingHTTPServer((a.host,a.port),partial(Handler,directory=str(ROOT/'web'))); print(f'http://{a.host}:{a.port}',flush=True); server.serve_forever()
if __name__=='__main__': main()
