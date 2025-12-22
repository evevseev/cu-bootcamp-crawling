# chitai_gorod

## Sample data 

Is located at [collection.json](./collection.json).

## Sample requests

## 200

```bash
curl 'http://127.0.0.1:8000/search_by_isbn?isbn=978-5-699-48580-2' | jq
```

```json
{
  "title": "Мертвые души. Повести",
  "author": "Николай Гоголь",
  "description": "Николай Васильевич Гоголь (1809-1852) — великий русский писатель, создатель особого, неповторимого стиля в литературе. Талант Гоголя проявляется во всех его произведениях по-разному — то поражает читателя богатством языка и украинским колоритом, как в \"Вечерах на хуторе близ Диканьки\", то увлекает фантастикой петербургских повестей, то вызывает смех, как в \"Ревизоре\" и \"Мертвых душах\".",
  "price_amount": 0,
  "price_currency": "RUB",
  "rating_value": 4.3,
  "rating_count": 9,
  "publication_year": 2017,
  "isbn": "978-5-699-48580-2",
  "pages_cnt": 768,
  "publisher": "Эксмо",
  "book_cover": "https://content.img-gorod.ru/pim/products/images/d5/e4/0199ece7-b076-7179-83c5-48437455d5e4.jpg?width=304&height=438&fit=bounds",
  "source_url": "https://www.chitai-gorod.ru/product/mertvye-dushi-povesti-2031009"
}
```

## 400

```bash
curl 'http://127.0.0.1:8000/search_by_isbn?isbn=978-5-699-48580-1' | jq
```

```json
{
  "detail": "Can't find book with this ISBN"
}
```