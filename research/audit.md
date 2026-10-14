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
