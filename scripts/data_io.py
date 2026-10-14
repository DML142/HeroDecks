"""Read/save the hero-sharded analysis catalog, accepting the original flat format."""
import json,pathlib

def read_data(root,path):
 root=pathlib.Path(root);data=json.loads((root/path).read_text())
 if path=='data/deck-analysis.json' and data.get('schema')=='herodecks-analysis-v2':
  out={}
  for shard in data['files']:
   part=json.loads((root/shard).read_text())
   if out.keys() & part.keys():raise ValueError('Duplicate analysis IDs between shards')
   out.update(part)
  return out
 return data

def save_analysis(root,analysis):
 root=pathlib.Path(root);directory=root/'data/deck-analysis';directory.mkdir(exist_ok=True)
 heroes=sorted({key.split('/')[0] for key in analysis});files=[]
 for hero in heroes:
  path='data/deck-analysis/'+hero+'.json';files.append(path)
  part={key:val for key,val in analysis.items() if key.split('/')[0]==hero}
  (root/path).write_text(json.dumps(part,ensure_ascii=False,indent=2)+'\n')
 (root/'data/deck-analysis.json').write_text(json.dumps(dict(schema='herodecks-analysis-v2',decks=len(analysis),files=files),ensure_ascii=False,indent=2)+'\n')
