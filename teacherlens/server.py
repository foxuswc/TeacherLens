from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import json, argparse
from .core import ROOT, load, grade, record_review
class Handler(SimpleHTTPRequestHandler):
    def send_json(self,obj,status=200):
        body=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/demo': return self.send_json(load(ROOT/'data/demo.json'))
        return super().do_GET()
    def do_POST(self):
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n>1_000_000: return self.send_json({'error':'请求过大'},413)
            d=json.loads(self.rfile.read(n))
            if self.path=='/api/grade':
                rows=[grade(d['task'],a,d['rubric'],d.get('mode','calibrated'),d.get('engine','demo')) for a in d['answers']]; return self.send_json(rows)
            if self.path=='/api/review': return self.send_json(record_review(d['result'],d['score'],d['reason'],d['scope']))
            return self.send_json({'error':'not found'},404)
        except Exception as e: return self.send_json({'error':str(e)},400)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--port',type=int,default=8765); a=p.parse_args(); server=ThreadingHTTPServer(('127.0.0.1',a.port),partial(Handler,directory=str(ROOT/'web'))); print(f'http://127.0.0.1:{a.port}',flush=True); server.serve_forever()
if __name__=='__main__': main()
