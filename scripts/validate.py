#!/usr/bin/env python3
"""Validate deck legality, metadata coverage, generated lists and local links."""
import pathlib,json,re,collections,math
R=pathlib.Path(__file__).resolve().parents[1]
from data_io import read_data,save_analysis
read=lambda p:read_data(R,p)
C={c['id']:c for c in read('data/cards.json')};H={h['id']:h for h in read('data/heroes.json')};D=read('data/decks.json');A=read('data/deck-analysis.json');P=read('data/card-analysis.json');PW={p['name']:p for p in read('data/powers.json')};corpus={x['id']:x for x in read('research/meta-corpus.json')}
errors=[];warnings=[]
def require(ok,msg):
 if not ok:errors.append(msg)
def slug(s):return re.sub('[^a-z0-9]+','_',s.lower()).strip('_')
require(len(C)==503,'card universe must contain 503 records');require(len(H)==22,'must contain all 22 heroes');require(len(D)==330,'must contain 330 deck files')
require(len({d['id'] for d in D})==len(D),'duplicate deck IDs')
require(set(A)=={d['id'] for d in D},'analysis/deck IDs differ')
require(len({tuple(sorted((x['card'],x['count']) for x in d['cards'])) for d in D})==330,'exact list duplicates')
metrics={x['id'] for x in read('data/rating-metrics.json')}; require(len(metrics)==15,'must have 15 rating metrics')
require(sum(d.get('theme',False) for d in D)==10,'must have 10 hero-specific theme builds')
for h in H.values():
 powers=[h['signature']]+h['powers'];require(len(powers)==4 and len(set(powers))==4,h['id']+' powers count')
 require(all(p in PW and h['id'] in PW[p]['heroes'] for p in powers),h['id']+' power ownership')
 require(sum(d['hero']==h['id'] for d in D)==15,h['id']+' must have exactly 15 decks')
for d in D:
 h=H[d['hero']];ids=[e['card'] for e in d['cards']];n=sum(e['count'] for e in d['cards'])
 require(n==40,d['id']+' total '+str(n));require(len(ids)==len(set(ids)),d['id']+' duplicate rows')
 path=R/'decks'/h['faction']/h['id']/(d['slug']+'.md');require(path.exists(),d['id']+' missing Markdown')
 text=path.read_text() if path.exists() else ''
 for e in d['cards']:
  c=C.get(e['card']);require(c is not None,d['id']+' unknown card');require(type(e['count']) is int and 1<=e['count']<=4,d['id']+' copies')
  if c:
   require(c['faction']==h['faction'] and c['class'] in h['classes'],d['id']+' wrong class '+c['name'])
   require(c['deckable'],d['id']+' uncollectible card');require(c['id'] in P,d['id']+' missing card analysis')
   require(f"### {e['count']}× {c['name']}" in text,d['id']+' count section mismatch')
   require(f"{e['count']}x {c['name']}" in text,d['id']+' export list mismatch')
 if d.get('source_id') and not d.get('changes'):
  a=sorted((x['card'],x['count']) for x in d['cards']);b=sorted((x['card'],x['count']) for x in corpus[d['source_id']]['cards']);require(a==b,d['id']+' differs from sourced list')
 if d.get('changes'):
  base=next(x for x in D if x['id']==d['base_id']);m={x['card']:x['count'] for x in base['cards']}
  for ch in d['changes']:m[ch['card']]=m.get(ch['card'],0)+ch['delta']
  require({k:v for k,v in m.items() if v}=={x['card']:x['count'] for x in d['cards']},d['id']+' inaccurate delta')
  require(sum(x['delta'] for x in d['changes'])==0,d['id']+' nonzero replacement delta')
 ratings=A[d['id']].get('ratings',{}); require(set(ratings)==metrics,d['id']+' ratings coverage')
 for k,v in ratings.items():require(type(v.get('score')) is int and 1<=v['score']<=10 and bool(v.get('reason')),d['id']+' rating invalid '+k)
 require(bool(A[d['id']].get('semantic_checks')),d['id']+' no semantic premises')
 for z in A[d['id']].get('semantic_checks',[]):require(z['card'] in ids and bool(z['evidence']) and bool(z['limit']),d['id']+' invalid semantic check')
 if d['category']=='source-portfolio':require(d['selection_distance']>=9,d['id']+' too close to existing list at selection')
 for ev in A[d['id']].get('counter_evidence',[]):
  opponent=next((x for x in D if x['id']==ev['deck']),None)
  require(opponent is not None and set(ev['cards']).issubset({x['card'] for x in opponent['cards']}),d['id']+' incorrect opposing card package')
 for cid in ids:
  ev=re.search(r'(\w+(?:-\w+)?) Evolution',C[cid]['effect'])
  if ev:
   tag=ev[1];bases=[k for k in ids if (k!=cid or next(z['count'] for z in d['cards'] if z['card']==cid)>=2) and (('Team-Up' in C[k]['effect']) if tag=='Team-Up' else tag in C[k]['type'].split())]
   require(bool(bases),d['id']+' lacks '+tag+' Evolution support for '+cid)
 for section in ['construction','hero_reason','mulligan','early','mid','late','combo','counters','mistakes']:require(bool(A[d['id']].get(section)),d['id']+' missing section '+section)
 for section in ['Мышление при создании','Почему именно этот герой','Каждая карта','Как играть','Контрколоды','Итоговый список']:require(section in text,d['id']+' Markdown section absent '+section)
for hid,h in H.items():
 if 'Brainy' in h['classes']:require(any(d['hero']==hid and d.get('theme') and 'Bad_Moon_Rising' in [x['card'] for x in d['cards']] for d in D),hid+' lacks tailored BMR')
 if 'Guardian' in h['classes']:require(any(d['hero']==hid and d.get('theme') and {'Force_Field','Soul_Patch'}.issubset({x['card'] for x in d['cards']}) for d in D),hid+' lacks tailored Force Patch')
for c in C.values():
 require(c['wiki_url'] and c['wiki_url'].startswith('https://plantsvszombies.wiki.gg/'),c['id']+' missing wiki source')
 require(type(c['cost']) is int and c['cost']>=0,c['id']+' invalid cost')
 require(bool(c['effect']),c['id']+' empty rule')
 path=R/'cards'/c['faction']/slug(c['class'])/(slug(c['name'])+'.md');require(path.exists(),c['id']+' no card file')
 if c['evidence']=='wiki-search-excerpt':warnings.append(c['name']+': only partial wiki excerpt; current client not verified')
linkcount=0
for path in R.rglob('*.md'):
 if 'raw' in path.parts:continue
 for dest in re.findall(r'\]\(([^\s)]+)\)',path.read_text()):
  if re.match(r'^(https?://|#|mailto:)',dest):continue
  target=(path.parent/dest.split('#')[0]).resolve();linkcount+=1;require(target.exists(),str(path.relative_to(R))+' broken link '+dest)
# Focused invariant checks for reviewed interactions; they do not simulate the game.
require(C['Espresso_Fiesta']['cost']==7,'Espresso source mismatch')
require(C['Pea_Patch']['type'].find('Pea')>=0 and 'Leafy' in C['Pea_Patch']['type'],'Patch evolution tags')
require('Pea' in C['Gatling_Pea']['type'] and 'Pea' not in C['Bonk_Choy']['type'],'Pea Evolution premise')
require('Team-Up' in C["Li'l_Buddy"]['effect'] and 'Team-Up Evolution' in C['Cob_Cannon']['effect'],'Cob evolution premise')
require('Untrickable' in C['Gravitree']['effect'] and 'Untrickable' in C['Apotatosaurus']['effect'],'Untrickable rules')
require('Zombie Evolution' in C['Primordial_Cheese_Shover']['effect'],'Shover body-removal premise')
require('Mustache' in C['Bungee_Plumber']['type'],'Waxer trigger tag')
require('+2 Health' in C['Mustache_Waxer']['effect'],'Waxer current +2 Health')
require('Trick' in C['Teleport']['type'] and C['Teleport']['class']=='Brainy','Teleport legality')
require(abs((1-math.comb(39,4)/math.comb(40,4))*100-10)<1e-9,'opening probability arithmetic')
report={'date':'2026-10-14','status':'pass' if not errors else 'fail','heroes':len(H),'decks':len(D),'cards':len(C),'ratings_per_deck':len(metrics),'semantic_checks':sum(len(A[d['id']]['semantic_checks']) for d in D),'powers':len(PW),'corpus_entries':len(corpus),'checked_local_links':linkcount,'errors':errors,'warnings':warnings,'limits':'Structural checks and selected semantic premises only. No gameplay simulation, client replay or win-rate measurement.'}
(R/'validation').mkdir(exist_ok=True);(R/'validation/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['warnings']},ensure_ascii=False,indent=2));print('Partial-source warnings:',len(warnings))
raise SystemExit(bool(errors))
