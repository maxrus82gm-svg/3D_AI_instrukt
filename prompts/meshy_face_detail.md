# Meshy Agent — сохранение возрастного лица, детализация и два референса

**Кейс:** Аластор «Грозный Глаз» Грюм; 10.10.2026.  
**Самый важный результат дня:** высокодетализированный вариант **изображения** головы сохранил тяжёлую челюсть, возраст, суровое лицо, складки, шрамы и механический окуляр. Это и был удачный визуальный ориентир. Генерация новой 3D-геометрии по составному изображению не гарантировала ту же точность.

Ниже — **восстановленные шаблоны по ходу диалога**, не буквальная стенограмма отправленных команд.

## 1. Базовый промпт: не терять сходство лица

```text
Use the provided image as the main and authoritative reference
for the character's face and overall likeness.

Preserve the exact face likeness and mature, weathered appearance.
Keep the broad jawline, full cheeks, heavy facial proportions,
stern expression, forehead wrinkles, eyelid folds, facial scars,
and the mechanical eyepatch with its rim and details.
Do not make the face slimmer, younger, softer, smoother, or prettier.
Do not redesign the face or change the character's identity.

Increase the clarity of sculptural planes, deep facial creases,
eyepatch details, scars, hair grooves, collar edges, lapel seams,
and main clothing folds without changing their shape or proportions.

Keep the existing silhouette and hairstyle.
Hair must remain in thick connected sculpted locks,
not fragile separated strands.
Avoid excessive smoothing and loss of sculpt detail.
```

## 2. Сведение двух 2D-референсов

- **Левый образец:** правильная монолитная форма волос — широкие соединённые скульптурные пряди, без отдельных тонких нитей.
- **Правый образец:** более тонкая проработка поверхности — морщины, шрамы, окуляр, складки и швы одежды.
- **Что должно сохраниться:** возрастное лицо, общее сходство и пропорции, силуэт причёски и бюста.
- В интерфейсе Meshy Agent использовался этап **«Изображение в изображение»** с двумя референсами. На сохранившемся скриншоте видна модель **GPT Image 2.5 Sunburst** (в интерфейсе название обрезано как «GPT Image 2.5 Sunbu...»). Это настройка **изображения**, не 3D-генератора.

### Промпт для сведения (восстановлен, EN)

```text
Combine the two provided reference images into one final,
high-definition sculpt reference for the same character.

Use the LEFT image for the solid connected printable hair locks:
thick sculpted masses, preserved hairstyle flow and outer silhouette,
no fine separated strands or fragile ends.

Use the RIGHT image for higher sculpt detail:
sharper forehead wrinkles, eyelid folds, facial scars,
metallic eyepatch rim and details, deeper hair grooves,
crisper collar and lapel seams, and readable fabric creases.

Preserve the exact overall form, proportions, mature facial likeness,
mechanical eyepatch, hairstyle silhouette, clothing,
and bust outline. Do not slim or rejuvenate the face.
Do not replace the robust hair with thin strands.
Enhance surface definition without changing the sculpture's shape.
```

## 3. Отдельная инструкция при переходе к 3D-бюсту

```text
Generate a new 3D bust model using the provided image
as the main and authoritative reference.

Preserve the exact face likeness, broad mature facial proportions,
wrinkles, scars, and mechanical eyepatch.
Do not make the face slimmer, younger, or softer.
Keep the hair in solid connected sculpted locks with readable grooves.
No thin strands. Preserve sharp sculpt detail.
Do not over-smooth the model.
```

Это сокращённая версия ранее обсуждавшегося задания; детали формулировки восстановлены, а не проверены по полному исходному отправленному запросу.

## Результат и граница применимости

1. **Удачно:** получен 2D-композит с возрастным, узнаваемым лицом и правильной массой волос.
2. **Не всегда повторилось:** при дальнейшей попытке получить полноценную модель/перекомпоновать голову и тело AI мог менять лицо.
3. **Практический обход:** взять удачную голову и корпус отдельными моделями, совместить и объединить вручную в **ZBrush**.
4. Для конечного размера **30 мм** высокочастотная фактура вторична; решают читаемая челюсть, окуляр, пряди и силуэт.

Связанные документы: [волосы](meshy_hair_sculpt.md), [кейс Грюма](../cases/mad_eye_moody.md).

> Статус: зафиксировано по истории и скриншотам от 10.10.2026. «Удачный промпт лица» здесь означает удачный **визуальный результат**, а не гарантию точного переноса в 3D.
