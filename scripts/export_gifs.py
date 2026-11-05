"""Rebuild GIFs from accepted RGBA frames; reserve palette index 255 for alpha."""
from pathlib import Path
from PIL import Image,ImageSequence
import json,zipfile
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'catalog/stickers.json').read_text())
for item in items:
 folder=root/'packs'/item['pack'];frames=[]
 for path in sorted((folder/'frames'/item['id']).glob('*.png')):
  rgba=Image.open(path).convert('RGBA')
  frame=rgba.convert('RGB').quantize(colors=255,method=Image.Quantize.MEDIANCUT)
  frame.putpalette(frame.getpalette()[:765]+[0,0,0])
  frame.paste(255,mask=rgba.getchannel('A').point(lambda a:255 if a<128 else 0))
  frame.info['transparency']=255;frames.append(frame)
 dest=folder/(item['id']+'.gif')
 frames[0].save(dest,save_all=True,append_images=frames[1:],duration=[350,250,350,250],loop=0,disposal=2,transparency=255,optimize=False)
 check=Image.open(dest);assert check.n_frames==4 and check.info['loop']==0
 for f in ImageSequence.Iterator(check):assert f.convert('RGBA').getpixel((0,0))[3]==0
 print(item['pack'],item['id'],'4 frames; transparent; loop OK')
with zipfile.ZipFile(root/'downloads/media-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
 for item in items:
  for kind in ['gif','png']:z.write(root/item[kind],item[kind])
with zipfile.ZipFile(root/'downloads/media-pack.zip') as z:assert z.testzip() is None
