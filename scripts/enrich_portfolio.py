#!/usr/bin/env python3
"""Add per-list semantic premises and concrete card comparisons."""
import json,pathlib,re,math,collections
R=pathlib.Path(__file__).resolve().parents[1]
from data_io import read_data,save_analysis
read=lambda p:read_data(R,p)
C={x['id']:x for x in read('data/cards.json')};H={x['id']:x for x in read('data/heroes.json')};D=read('data/decks.json');A=read('data/deck-analysis.json');E=read('data/archetypes.json')
comparisons={
 'Bad_Moon_Rising':('Evolutionary_Leap','Leap за 2 улучшает одно основание на стоимость +1 и даёт Draw; Moon за 7 меняет всё живое Zombie-поле в 5+. Здесь нужна массовая конверсия нескольких дешёвых тел, а не постепенное улучшение одного. Leap не заменяет этот payoff, но снижает число полностью мёртвых подготовительных ходов.'),
 'Force_Field':('Spikeweed_Sector','Spikeweed за 3 помогает разменам повреждением зомби; Force за 4 предотвращает повреждение ваших растений. Для перенаправленного урона Patch требуется именно предотвращение, поэтому более дешёвый атакующий ландшафт не воспроизводит защитную связку.'),
 'Soul_Patch':('Gravitree','Оба стоят 6. Gravitree 7/7 Armored 1 Untrickable лучше защищён от целевых трюков и влияет на позицию новых зомби, но не принимает урон героя. Patch 5/10 выбран ради этой уникальной защиты; Gravitree подходит для другого плана с давлением, а не прямой замены комбо.'),
 'Pecanolith':('Three-Nut','Three-Nut за 3 задаёт новым Plants атаку 3, Pecanolith за 5 заставляет обе стороны атаковать здоровьем. Здесь важна высокая Health существ, но ответные 5–9 здоровья Zombie тоже становятся угрозой. Ускорение Three-Nut безопаснее по темпу, но даёт меньший потолок этой конкретной оси.'),
 'Pineclone':('Molekale','Pineclone за 4 даёт предсказуемые 3/3 по числу тел, Molekale за 4 даёт случайных существ стоимостью +1 и сохраняет себя. Выбор Pineclone делает итог широкой конверсии стабильнее; Molekale покупает разброс результатов, а не ту же армию.'),
 'Molekale':('Pineclone','Pineclone за 4 даёт известные 3/3, Molekale за 4 сохраняет себя и меняет других Plants в случайных за +1 стоимости. Здесь выбран потолок и разнообразие результатов; если нужна стабильность, менять следует весь пакет оснований под Pineclone.'),
 'Trickster':('Kitchen_Sink_Zombie','Kitchen Sink за 6 имеет набор атакующих traits, но не получает скидку от ранее сыгранных Tricks и не повторяет When played-атаку Trickster. Здесь removal должен одновременно приближать финишер; дешёвая крупная угроза меняет двигатель всей колоды.'),
 'Winter_Squash':('Snapdragon','Snapdragon за 4 даёт splash-давление без второй карточки, Squash за 4 превращает Freeze в уничтожение. Squash выбран ради удаления независимо от больших характеристик; без поддержки заморозкой Snapdragon чаще самодостаточен.'),
 'Onion_Rings':('Apotatosaurus','Rings за 5 конвертирует несколько Plants в текущей руке в 4/4; Apotatosaurus за 6 — отдельная защищённая от трюков угроза. Здесь ценность распределена между последующими дешёвыми розыгрышами, поэтому один большой боец не даёт той же эффективности руки.'),
 'Gatling_Pea':('Bananasaurus_Rex','Rex за 4 имеет Double Strike и рост от получения карт, Gatling за 5 даёт бонусную атаку при Pea Evolution. Gatling выбран для немедленного удара из уже стоящего Pea; Rex требует иной поддержки и выживания до своих атак.'),
 'Mirror-Nut':('Pecanolith','Mirror-Nut за 4 превращает повреждение Nuts в 1 Bullseye-урон по герою, Pecan за 5 превращает здоровье в атаку обеих сторон. Первый выигрывает через hurt-триггеры, второй через сохранённое Health; менять их без пересборки пакета нельзя.'),
 'Parasol_Zombie':('Mad_Chemist','Оба стоят 4, но Parasol защищает себя/соседей от Plant Tricks, а Chemist ориентирован на ресурс трюков. Здесь важнее сохранить уже выставленный engine до боя, чем получить дополнительную случайную карту.'),
 'Umbrella_Leaf':('Sweet_Potato','Оба стоят 1 и имеют Team-Up, но Sweet Potato меняет расположение угроз, Leaf даёт другим растениям здесь/рядом Untrickable. В Patch-пакете нужен запрет целевых Zombie Tricks; Leaf сам этим запретом не защищён и environment replacement остаётся возможным.')}

AUD=[]
for d in D:
 a=A[d['id']];h=H[d['hero']];m={x['card']:x['count'] for x in d['cards']};rows=[]
 for cid,n in m.items():
  c=C[cid];ev=re.search(r'(\w+(?:-\w+)?) Evolution',c['effect'])
  if ev:
   tag=ev[1];bases=[k for k in m if (k!=cid or n>=2) and (('Team-Up' in C[k]['effect']) if tag=='Team-Up' else tag in C[k]['type'].split())]
   assert bases,(d['id'],cid,tag)
   bases.sort(key=lambda k:(C[k]['cost'],-m[k]))
   rows.append(dict(card=cid,check=f'{tag} Evolution',evidence=', '.join(f"{m[k]}× {C[k]['name']}" for k in bases),limit=f"Если {C[bases[0]]['name']} ставится в тот же ход, напечатанная сумма {C[bases[0]]['cost']} + {c['cost']} = {C[bases[0]]['cost']+c['cost']}. Нужны свободная линия, выжившее основание и отсутствие запрещающего эффекта; его стоимость не исчезает от Evolution."))
 for cid,tag in [('Mustache_Waxer','Mustache'),('Gadget_Scientist','Science'),('Captain_Flameface','Pirate'),('Imp_Commander','Imp'),('Toxic_Waste_Imp','Imp'),('Zookeeper','Pet'),('Briar_Rose','Flower'),('Admiral_Navy_Bean','Bean'),('Starch_Lord','Root'),('Team_Mascot','Sports')]:
  if cid in m:
   targets=[k for k in m if tag in C[k]['type'].split()];num=sum(m[k] for k in targets)
   rows.append(dict(card=cid,check=f'{tag}-поддержка',evidence=f"{num} слотов: "+', '.join(C[k]['name'] for k in targets),limit='Типы взяты из карточного каталога. Число — плотность подходящих карт, не число гарантированных триггеров; конкретный момент и необходимость живого носителя остаются по тексту правила.'))
 if 'Winter_Squash' in m:
  freeze=[k for k in m if k!='Winter_Squash' and 'freeze' in C[k]['effect'].lower()];assert freeze
  rows.append(dict(card='Winter_Squash',check='Freeze после payoff',evidence=', '.join(C[k]['name'] for k in freeze),limit='Нужно событие заморозки при уже живом Squash; ранняя заморозка не сохраняется как будущий триггер уничтожения.'))
 if 'Bad_Moon_Rising' in m:
  body=sum(n for k,n in m.items() if C[k]['strength'] is not None)
  rows.append(dict(card='Bad_Moon_Rising',check='Основания и ресурс',evidence=f'{body} слотов существ; напечатанная цена BMR 7',limit='Слоты не равны одновременно выжившим телам. Даже четыре дешёвых Zombie не гарантируют четырёх полезных результатов; один Vendor без среды даёт чистый 0, а не +3 свободного ресурса.'))
 if all(k in m for k in ['Force_Field','Soul_Patch']):
  rows.append(dict(card='Soul_Patch',check='Перенаправление и предотвращение',evidence='Soul Patch 6 + Force Field 4 = 10; только ground',limit='Damage перенаправляется в Patch и предотвращается полем. Destroy, bounce, transform, перенос и замена среды требуют отдельного ответа. Защита не даёт автоматического летала.'))
 if 'Synchronized_Swimmer' in m:
  samples=sorted([k for k in m if k!='Synchronized_Swimmer' and C[k]['strength'] is not None],key=lambda k:(C[k]['strength'] or 0)+(C[k]['health'] or 0),reverse=True)
  rows.append(dict(card='Synchronized_Swimmer',check='Живой образец',evidence=', '.join(f"{C[k]['name']} {C[k]['strength']}/{C[k]['health']}" for k in samples[:3]),limit='Копируются текущие числовые Attack/Health, а не traits/abilities. Уничтоженный образец недоступен; нельзя считать скопированными Untrickable, Frenzy или Bullseye.'))
 if 'Nibble' in m:
  a['mistakes']=list(dict.fromkeys(a['mistakes']+['Nibble: в найденных материалах описан softlock против When destroyed-целей. Не включать зависимость от этого бага в выигрышную последовательность; применение к таким целям требует клиентского перепроверения.']))
 if 'Pecanolith' in m and 'Force_Field' in m:
  a['mistakes']=list(dict.fromkeys(a['mistakes']+['Pecanolith усиливает атакующее число ЗОМБИ тоже; Force Field предотвращает повреждения только вашей ground-линии. Проверять обе стороны до установки Pecan.']))
 if 'Mirror-Nut' in m and 'Force_Field' in m:
  a['mistakes']=list(dict.fromkeys(a['mistakes']+['Force Field предотвращает hurt ваших Nuts в своей линии: от предотвращённого повреждения Mirror-Nut не получает триггер. Разделять роли защиты Patch и отражающего урона Nuts.']))
 # Add a concrete first two-card resource checkpoint to EVERY list.
 sortedb=sorted((k for k in m if C[k]['strength'] is not None),key=lambda k:(C[k]['cost'],-m[k]))
 if len(sortedb)>=2:
  b1,b2=sortedb[:2];cost=C[b1]['cost']+C[b2]['cost']
  rows.append(dict(card=b1,check='Ранний ресурсный checkpoint',evidence=f"{C[b1]['name']} + {C[b2]['name']}: {C[b1]['cost']} + {C[b2]['cost']} = {cost}",limit='Напечатанная сумма без скидок/налога. Это пример доступных ранних тел, а не обещание обязательного хода или автоматическая синергия; выбор линий определяется конкретным боем.'))
 a['semantic_checks']=rows
 # Actual two-component access probability, without presenting it as board setup.
 core=[k for k in E[d['family']]['core'] if k in m]
 if d.get('theme') and d['family']=='force_patch':core=['Force_Field','Soul_Patch']
 if len(core)>=2:
  x,y=core[:2];nx,ny=m[x],m[y];draws=10
  prob=1-math.comb(40-nx,draws)/math.comb(40,draws)-math.comb(40-ny,draws)/math.comb(40,draws)+math.comb(40-nx-ny,draws)/math.comb(40,draws)
  a['package_access']=f"Хотя бы одна {C[x]['name']} и одна {C[y]['name']} среди первых 10 обычных выборок: {prob*100:.1f}% при {nx}×/{ny}×. Без mulligan, генерации, добора вне этих выборок и изменения колоды. Это доступ к двум именам, не вероятность успешно поставить/сохранить комбинацию."
 else:a['package_access']='Один основной payoff не заменяет наличие живых оснований и достаточного ресурса. Вероятность доступа к каждому имени приведена в карточном разборе; вероятность выиграть из неё не выводится.'
 if d['category'] in ['source-portfolio','theme-theorycraft']:
  for cid,(alt,why) in comparisons.items():
   if cid in m and C[alt]['class'] in h['classes']:a['card_alternatives'][cid]=why+' '+f"[{C[alt]['name']}]({C[alt]['wiki_url']}) — карточная проверка альтернативы."
  if 'Half-Banana' in m:a['card_roles']['Half-Banana']='При уничтожении усиливает Fruits в текущей руке на +1/+1. Не баффает уже стоящие Fruits и не работает от bounce/transform; держите будущие Fruit-угрозы в руке до нужного события.'
  if 'Brain_Vendor' in m:a['card_roles']['Brain_Vendor']='За 3 даёт тело 2/1 и возвращает 3 Brain в том же ходу: чистая цена по ресурсу 0 при возможности первоначально оплатить 3. С Medulla получает ещё +2, с Flag стоит меньше; поздний вход через Teleport/TZ уменьшает риск потерять основание до BMR. Сам по себе не увеличивает ресурс на чистые +3.'
  if 'Teleportation_Zombie' in m:a['card_roles']['Teleportation_Zombie']='Живой носитель разрешает играть Zombies в Tricks. Сохраняйте его до будущего Vendor/финишера; после уничтожения разрешение пропадает. Gravestone и 1/5 Bullseye — отдельные свойства, не постоянная неуязвимость.'
  if 'Umbrella_Leaf' in m:a['card_roles']['Umbrella_Leaf']='Team-Up за 1 даёт Untrickable ДРУГИМ Plants здесь и рядом. Сам Leaf своим эффектом не защищён; Force Field предотвращает его повреждение, но среда может быть заменена. Чужие способности существ обходят Untrickable.'
  if 'Gadget_Scientist' in m:a['card_roles']['Gadget_Scientist']='При розыгрыше каждый Science Zombie, включая самого Gadget, делает Bonus Attack. Плотность настоящих Science проверена ниже; появление карты с похожей технологической темой без Science-типа не даёт дополнительный удар.'
  if 'Captain_Flameface' in m:a['card_roles']['Captain_Flameface']='Даёт Strikethrough всем вашим Pirates, включая самого себя по текущему тексту. Сохраняйте его до боя; способность не превращает непиратов в Pirates и не убирает блок героя.'
  if 'Elderberry' in m:a['card_roles']['Elderberry']='Strikethrough 2/3 за 4; Plant Evolution даёт +3 Attack, поэтому основанием может быть любое подходящее растение, не только Flower. Потеря основания входит в обмен, а блок героя всё ещё может остановить урон.'
 AUD.append(dict(id=d['id'],hero=d['hero'],checks=len(rows),partial_sources=[x['card'] for x in d['cards'] if C[x['card']]['evidence']=='wiki-search-excerpt']))
overrides=read('data/editorial-card-roles.json')
labels={'early_body':'раннего бойца','late_body':'поздней угрозы','resource_body':'бойца с поддержкой руки','answer':'точечного/условного ответа','trick':'полезного трюка','environment':'контроля ground-линии'}
for a in A.values():
 if 'card_roles' not in a:continue
 for cid,txt in a['card_roles'].items():
  for k,v in labels.items():txt=txt.replace('своей функцией '+k,'своей функцией '+v)
  a['card_roles'][cid]=overrides.get(cid,txt)
 prefix='Классовые инструменты героя (не все обязательно включены в эти 40): '
 if not a['hero_reason'].startswith(prefix):a['hero_reason']=prefix+a['hero_reason']
save_analysis(R,A)
(R/'research/portfolio-audit.json').write_text(json.dumps(AUD,ensure_ascii=False,indent=2)+'\n')
print('Semantic premises',sum(x['checks'] for x in AUD),'for',len(AUD),'decks')
