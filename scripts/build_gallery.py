"""Build a searchable offline gallery and a media ZIP from catalog/stickers.json."""
from pathlib import Path
from html import escape
import json,zipfile
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'catalog/stickers.json').read_text());packs={x['pack']:x['outfit'] for x in items}
def esc(s):return escape(s,quote=True)
cards=''.join('<article data-pack="'+esc(x['pack'])+'" data-search="'+esc(x['caption']+' '+x['outfit'])+'"><img loading="lazy" src="'+esc(x['gif'])+'" alt="'+esc(x['caption'])+'"><h3>'+esc(x['caption'])+'</h3><p>'+esc(x['outfit'])+'</p><a download href="'+esc(x['gif'])+'">保存GIF</a> · <a download href="'+esc(x['png'])+'">保存PNG</a></article>' for x in items)
options=''.join('<option value="'+esc(p)+'">'+esc(t)+'</option>' for p,t in packs.items())
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>林知夏 · 表情衣橱</title><style>body{background:#f6eee8;color:#633d2e;font-family:system-ui;margin:24px auto;max-width:1100px;padding:16px}h1{font-size:32px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px}article{background:#fff9f4;border-radius:16px;text-align:center;padding:12px}article[hidden]{display:none}img{width:100%;image-rendering:pixelated}h3,p{margin:6px}a{color:#895941}select,input{padding:10px;margin:16px 8px 16px 0;border:1px solid #cbb6a4;border-radius:8px;background:#fff9f4;color:#633d2e}</style><h1>林知夏 · Q版表情衣橱</h1><p>COUNT套穿搭 · TOTAL款透明动态表情 · AI辅助制作</p><label>穿搭 <select id="filter"><option value="all">全部系列</option>OPTIONS</select></label><label>搜索 <input id="search" placeholder="输入表情或穿搭关键词"></label><p id="count">显示TOTAL款</p><main>CARDS</main><script>function update(){let n=0;const p=document.getElementById("filter").value,q=document.getElementById("search").value.trim();document.querySelectorAll("article").forEach(a=>{a.hidden=(p!=="all"&&a.dataset.pack!==p)||(q&&!a.dataset.search.includes(q));if(!a.hidden)n++});document.getElementById("count").textContent="显示"+n+"款"}document.getElementById("filter").onchange=update;document.getElementById("search").oninput=update</script></html>'''
page=page.replace('COUNT',str(len(packs))).replace('TOTAL',str(len(items))).replace('OPTIONS',options).replace('CARDS',cards)
(root/'index.html').write_text(page)
archive=root/'downloads'/f'stickers-{len(items)}.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 z.write(root/'index.html','index.html');z.write(root/'RIGHTS.md','RIGHTS.md')
 for x in items:
  for kind in ['gif','png']:
   source=root/x[kind];assert source.is_file(),source;z.write(source,x[kind])
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(f'Gallery: {len(items)} stickers / {len(packs)} outfits; ZIP: {archive.name}')
