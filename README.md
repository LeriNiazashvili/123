# Shop Project — განახლება

## რა დაემატა ამ ეტაპზე

1. **Templates** — `store/templates/store/base.html` (ნავბარი + სვეტი, screenshot-ის სტილში) და `store/templates/store/home.html` (პროდუქტების ბადე — გამოიყენება სამივე view-სთვის: `home`, `category_products`, `discounted_products`)
2. **CSS** — `static/css/style.css`, ორანჟისფერი ნავბარი, მუქი გვერდი
3. **Django Debug Toolbar** — დაყენებულია და მუშაობს (მხოლოდ `DEBUG=True`-ზე, `127.0.0.1`-დან)
4. **Context processor** (`store/context_processors.py`) — `latest_products` ცვლადი ავტომატურად ხელმისაწვდომია **ყველა** template-ში, ბოლოს დამატებული 5 პროდუქტს აბრუნებს
5. **ბაგის გასწორება**:
   - `seed.py`-ში იყო არასწორი import (`from store import ...` → გასწორდა `from store.models import ...`)
   - `discounted_products` view-ში `annotate`-ის key არ ემთხვეოდა სხვა view-ებს (`products_count` → `product_count`), რის გამოც sidebar-ის კატეგორიების რაოდენობა ფასდაკლების გვერდზე არ გამოჩნდებოდა

## როგორ გავუშვათ

```
cd shop_project
pip install -r requirements.txt
python manage.py runserver
```

გახსენი `http://127.0.0.1:8000/` — **მნიშვნელოვანია 127.0.0.1 გამოიყენო `localhost`-ის ნაცვლად**, რომ Debug Toolbar ჩანდეს (ის მხოლოდ `INTERNAL_IPS`-ში მითითებულ მისამართს ენდობა).

ბაზა (`db.sqlite3`) უკვე შეიცავს პროდუქტებს — ხელახლა seed-ის გაშვება არ არის სავალდებულო, მაგრამ თუ გინდა:
```
python manage.py shell < store/seed.py
```

## რა ჩანს გვერდზე

- **ნავბარი** — Home, Shop, Discounted, Shop Cart / Checkout / Contact (ეს ბოლო სამი მხოლოდ დიზაინისთვისაა, ფუნქციონალი მათზე არ არსებობს პროექტში)
- **მარცხენა სვეტი (sidebar)** — ყველა კატეგორია პროდუქტების რაოდენობით + "ბოლოს დამატებული 5 პროდუქტი" (context processor-იდან)
- **მთავარი არეალი** — პროდუქტების ბადე, ფასდაკლებული პროდუქტები წითელი ჩარჩოთი და "ფასდაკლება" badge-ით მონიშნული

## Debug Toolbar სად ჩანს

გვერდის მარჯვენა მხარეს, პატარა პანელი გამოჩნდება (SQL queries, Templates, Time და სხვ.) — ეს დაგეხმარება ნახო, რამდენი query გაეშვა ერთ გვერდზე და საიდან მოვიდა შენელება, თუ იქნება.
