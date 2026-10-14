# Журнал логической проверки и исправлений

## Исправленные расхождения

| Ошибка / риск | Принятое исправление | Основание |
| --- | --- | --- |
| Старый Pear Cub без усиления Fruit | Добавлен death-buff и Grizzly 6/5 после собственного Fruit-бонуса | [Pear Cub](https://plantsvszombies.wiki.gg/wiki/Pear_Cub) |
| Gravitree без Untrickable в secondary-базе | Включена текущая защита, отдельно указаны body-removal исключения | [Gravitree](https://plantsvszombies.wiki.gg/wiki/Gravitree) |
| Starch-Lord растит только новую Root | Указан рост самого Starch-Lord | [Starch](https://plantsvszombies.wiki.gg/wiki/Starch-Lord) |
| Waxer +1 Health из старого JSON | Исправлено на +2 Health и +1 Brain | [Waxer](https://plantsvszombies.wiki.gg/wiki/Mustache_Waxer) |
| Парсер отсёк вторую строку ability | Восстановлены Cob Team-Up Evolution, Jelly Bean Evolution, Dr. on-hit Conjure | Индивидуальные карточные файлы |
| Название Fig/Teacher/Viking вместо официального | Нормализованы Transfiguration/Zombology Teacher/Shieldcrusher Viking; исходный ID сохранён | Вики и alias-map |
| Похожий Trick-Stache был Brainy/Sneaky | Не включён под Professor Brainstorm; выбран Crazy/Brainy Trickstache | Проверка классов |
| Fiesta ошибочно «стоимость 1» | Используется 7; официальный patch wording не принят без сверки | [Espresso](https://plantsvszombies.wiki.gg/wiki/Espresso_Fiesta) |
| Frozen Tundra только ground | Используется all Plants по новой записи | [Frozen Tundra](https://plantsvszombies.wiki.gg/wiki/Frozen_Tundra) |
| Power Pummel автоматически damage герою | Принят текущий wiki-текст по зомби ground | [Power Pummel](https://plantsvszombies.wiki.gg/wiki/Power_Pummel) |
| Final Mission как четыре face-damage | По текущему источнику damage направлен в Plant | [Final Mission](https://plantsvszombies.wiki.gg/wiki/Final_Mission) |
| Fruitcake старые семь повреждений | В текущей записи пять; gifting Fruit указан как цена | [Fruitcake](https://plantsvszombies.wiki.gg/wiki/Exploding_Fruitcake) |
| Swimmer копирует все traits | Копируются только Strength/Health | [Swimmer](https://plantsvszombies.wiki.gg/wiki/Synchronized_Swimmer) |
| Terror-Former скидка всем зомби | Скидка Tricks/Environments в текущей руке | [сила](https://plantsvszombies.wiki.gg/wiki/Terror-Former_10%2C000) |
| Blob считает остаток brains | Считает полученное за ход; остаток отдельно нужен для оплаты | [Blob](https://plantsvszombies.wiki.gg/wiki/Zom-Blob) |
| Late counterpart выдавался за свежий лидирующий deck | Snapshot-даты и несовпадения названий отмечены | [мета](meta.md) |

## Границы проверки

Автоматическая проверка не играет матчи и не доказывает оптимальность количеств. Полнота wiki-excerpt ниже полноты клиентской записи. Сложные transform/Make-триггеры, сохранение статов после bounce отдельных карт и актуальность багов требуют отдельного клиента. Nibble-softlock не используется как «выигрышная синергия».

Результат проверки структуры записывается в `validation/report.json`. Каждый авторский countermeta-список сохраняет 40 и имеет явно указанную потерю в других матчапах.

## Портфель 330 и тематические проверки — 14.10.2026

- Ровно 15 списков каждому из 22 героев; все 330 численных составов различаются.
- По одному специально адаптированному BMR каждому Brainy и Force Field + Soul Patch каждому Guardian: [маршруты и контры](themes.md).
- BMR превращает в случайных за 5+, не 6+ и не гарантированного Zombot. Vendor за 3 возвращает 3; один Vendor в заранее установленной Medulla на обычном четвёртом ходу оставляет 6, поэтому раннее BMR требует дополнительного условия.
- Force 4 + Patch 6 = 10, добавление Umbrella 1 = 11. Ground-only для среды; уничтожение, bounce, перенос и environment replacement не объявлены предотвращённым уроном.
- Elderberry — **Plant Evolution**, не Flower Evolution. Gadget Scientist атакует вместе с остальными Science; текущий Flameface даёт Strikethrough всем Pirates, включая себя. Неправильные формулировки исправлены до публикации.
- Mirror-Nut не получает hurt-триггер от предотвращённого Force Field повреждения. Pecan меняет атакующее число у обеих сторон. Эти конфликтующие механики отдельно описаны в содержащих их списках.
- 622 индивидуальные структурно-семантические предпосылки: основания Evolution, реальные племенные типы, поддержка Freeze, образцы Swimmer и ресурсные checkpoint. Они не равны 622 проверенным партиям.
- 15 оценок на список; формулы и смысл направления открыты. Ни одна оценка не представлена измеренным винрейтом.

[Машинный свод](portfolio-summary.json) · [Предпосылки по спискам](portfolio-audit.json) · [Рейтинговая методика](ratings.md).

Фактические пакеты контрколод также сверены с их опубликованными 40: **894 сопоставления** для новых source/theme-разборов. Исправлены расширительные ссылки на Black-Eyed Pea в Sensei и Blockbuster в Amphibious Momentus (в этих конкретных базовых списках их нет). Telepsterrazzi угрожает Patch через Rocket Science и Rolling Stone против Umbrella; обычной среды в его конкретной версии нет. Возможные ответы других версий не выдаются за карты данного списка. Проверка хранится в `counter_evidence` разборов и в валидаторе.
