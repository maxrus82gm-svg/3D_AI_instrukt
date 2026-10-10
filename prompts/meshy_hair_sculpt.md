# Meshy Agent — массивные скульптурные волосы

**Кейс:** бюст Аластора «Грозный Глаз» Грюма (Mad-Eye Moody), 10.10.2026.  
**Статус:** приём дал удачное изображение/бюст с цельными прядями; ниже **восстановленная рабочая версия**, не претендует на дословную копию всей первоначальной команды. Некоторые ключевые фразы сохранены дословно из истории.

## Задача

Заменить слишком тонкие, висящие и раздельные AI-пряди на крупные, цельные и физически соединённые скульптурные локоны, подходящие для уменьшения и 3D-печати. Лицо, окуляр, шрамы, одежду и силуэт головы не перерисовывать.

## Рабочий промпт (восстановленная версия, EN)

```text
Modify only the hair on the selected model.

Preserve the current face exactly as it is now.
Do not slim the face, do not make the character younger,
and do not soften or reinterpret the character's identity.
Preserve the broad mature facial proportions, heavy jawline,
full cheeks, wrinkles, scars, mechanical eyepatch, and expression.

Preserve the existing hairstyle silhouette, length, height,
width, direction, and overall flow. Do not add extra volume
or puffiness on the top or sides.
Maintain the slight outward flare of the lower hair toward the shoulders.

Convert the current thin, separated hair strands into
thicker, connected, sculpted, 3D-printable hair forms.
Use large unified sculpted locks: broad, chunky, flowing
wavy forms with readable sculpted grooves between them.
Make the locks physically connected to the main hair mass.
Eliminate flyaway strands, fragile thin tips, floating pieces,
hair-like filaments, and narrow unsupported gaps.

Keep a clear layered sculptural rhythm and deep readable grooves.
Do not turn the hair into a smooth helmet-like mass.
Do not change the forehead, facial outline, mechanical eye,
scars, neck, clothing, or bust proportions.

Important: change only the hair.
```

## Что оказалось критично

- **Локальная область:** `Modify only the hair on the selected model` — не разрешать нейросети заново интерпретировать всё лицо.
- **Защита возраста:** `Do not slim the face`, `do not make the character younger` — иначе терялось узнаваемое суровое возрастное лицо.
- **Форма прядей:** `large unified sculpted locks` — не просто «больше деталей», а цельные массивные локоны с отдельными бороздками.
- **Силуэт:** сохранить форму причёски, длину, объём сверху; внизу допускалось небольшое расширение наружу к плечам.
- **Физическая прочность:** убрать тонкие самостоятельные «волосинки», свободные кончики и пустоты между неустойчивыми нитями.
- **Чего избегать:** не надувать причёску и не превращать её в гладкий «шлем».

## Связанные материалы

- [Возрастное лицо и сочетание референсов](meshy_face_detail.md)
- [Практический результат: Грюм](../cases/mad_eye_moody.md)

> Надёжность записи: принципы и отдельные цитируемые английские фразы восстановлены из обсуждения 10.10.2026; полный исходный промпт, посланный в Agent, недоступен как точная посимвольная копия. Не подменять им оригинал, если впоследствии сохраним экспорт чата.
