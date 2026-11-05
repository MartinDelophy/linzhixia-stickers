"""Check catalog integrity and the actual decoded GIFs (requires Pillow)."""
from pathlib import Path
from PIL import Image,ImageSequence
import json,zipfile
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'catalog/stickers.json').read_text())
assert len(items)>=30
assert len({i['caption'] for i in items})==len(items)
for item in items:
 im=Image.open(root/item['gif'])
 assert im.size==(320,320) and im.n_frames==4 and im.info.get('loop')==0
 frames=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(im)]
 assert len({f.tobytes() for f in frames})>1
 for frame in frames:
  assert frame.getpixel((0,0))[3]==0
  bbox=frame.getbbox();assert bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<320 and bbox[3]<320,(item['id'],bbox)
 assert (root/item['png']).exists()
with zipfile.ZipFile(root/'downloads/stickers-30.zip') as z:
 assert z.testzip() is None
 assert sum(n.endswith('.gif') for n in z.namelist())==len(items)
 assert sum(n.endswith('.png') for n in z.namelist())==len(items)
print(f'PASS: {len(items)} unique stickers; decoded frames, alpha, padding, loops and ZIP verified')
