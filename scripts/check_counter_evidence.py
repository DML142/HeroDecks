#!/usr/bin/env python3
"""Attach factual opposing packages, without pretending matchup measurements."""
import pathlib,re,json
from data_io import read_data,save_analysis
R=pathlib.Path(__file__).resolve().parents[1];D=read_data(R,'data/decks.json');A=read_data(R,'data/deck-analysis.json');C={c['id']:c for c in read_data(R,'data/cards.json')}
normalize=lambda s:re.sub('[^a-z0-9]','',s.lower())
byname={normalize(d['name']):d for d in D}
focus={'sensei':['Forget-Me-Nuts','Gatling_Pea','Clique_Peas'],'healmidrose':['Brainana','Dark_Matter_Dragonfruit','Cob_Cannon'],'cyclecap':['Astro_Shroom','Planet_of_the_Grapes','Admiral_Navy_Bean'],'telimps':['Teleportation_Zombie','Toxic_Waste_Imp','Imp_Commander'],'trickstache':['Teleport','Trickster','Mustache_Waxer'],'midtomba':['Pogo_Zombie','Mixed-Up_Gravedigger','Black_Hole'],'amphibiousmomentus':['Cool_Bean','Navy_Bean','Marine_Bean'],'telepsterrazzi':['Rocket_Science','Rolling_Stone','Teacher'],'nohokai':['Laser_Base_Alpha','Space_Cowboy','Quickdraw_Con_Man']}
for d in D:
 a=A[d['id']];ev=[]
 if d['category'] not in ['source-portfolio','theme-theorycraft']:continue
 for row in a['counters']:
  name,why=row
  if normalize(name)=='sensei' and d['family']=='bmr':why='Forget-Me-Nuts повышает цену BMR, ранние Peas и Gatling Evolution ускоряют гонку. Сначала снимайте налог, затем пересчитывайте цену 7 плюс действующие ограничения; нельзя ждать Moon без блокеров.'
  if normalize(name)=='amphibiousmomentus':why='Cool Bean замораживает ваши надгробия и покупает водному полю один решающий бой. Marine/Navy создают давление по нескольким линиям; распределяйте скрытые вложения и не считайте anti-grave уже потраченным без наблюдения.'
  if normalize(name)=='telepsterrazzi' and d['family']=='force_patch':why='Rocket Science уничтожает Patch с атакой 5. Если Umbrella защищает его от трюков, Rolling Stone может сначала уничтожить сам Leaf с атакой 0: Force предотвращает damage, но не destroy. В этом точном Telepsterrazzi нет обычной среды; замена Force — отдельная угроза других версий Zombie, а не заявленная карта этого списка.'
  if normalize(name)=='midtomba' and d['family']=='force_patch':why='Pogo/MUG возвращают Patch, Sumo переносит его, Black Hole/Laser Base Alpha заменяют Force. Способность существа обходит Untrickable; удерживайте anti-grave до раскрытия, если он есть, и запасной атакующий маршрут.'
  why=re.sub(r' Фактический пакет найденного списка:.*$','',why)
  opponent=byname.get(normalize(name))
  if opponent:
   m={x['card']:x['count'] for x in opponent['cards']};cards=[c for c in focus.get(normalize(name),[]) if c in m]
   if cards:
    why+=' Фактический пакет найденного списка: '+', '.join(f"{m[c]}× {C[c]['name']}" for c in cards)+'.'
    ev.append(dict(deck=opponent['id'],cards=cards))
  row[1]=why
 a['counter_evidence']=ev
save_analysis(R,A)
print('Verified opposing packages',sum(len(a.get('counter_evidence',[])) for a in A.values()))
