from django.core.management.base import BaseCommand
from app.models import FAQ, Categories, Subcategories, Products


class Command(BaseCommand):
    help = 'Populates the database with initial data for the online tech store'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating the database...")

        # Создаем FAQ
        faqs = [
            {"question": "Как оформить заказ?", "answer": "Перейдите в корзину и нажмите 'Оформить заказ'."},
            {"question": "Как отследить заказ?", "answer": "Используйте номер заказа в личном кабинете."},
            {"question": "Какие способы оплаты доступны?", "answer": "Мы принимаем карты и наличные."},
            {"question": "Есть ли доставка?", "answer": "Да, доставка доступна по всему городу."},
            {"question": "Как вернуть товар?", "answer": "Обратитесь в службу поддержки."},
            {"question": "Какая гарантия на товар?", "answer": "Гарантия зависит от производителя."},
            {"question": "Как связаться с поддержкой?", "answer": "Напишите нам в Telegram."},
            {"question": "Есть ли скидки?", "answer": "Да, скидки доступны для постоянных клиентов."},
            {"question": "Как узнать статус заказа?", "answer": "Проверьте статус в личном кабинете."},
            {"question": "Можно ли изменить заказ?", "answer": "Да, до момента отправки."},
        ]
        for faq in faqs:
            FAQ.objects.create(**faq)
        self.stdout.write(self.style.SUCCESS('10 FAQ objects created'))

        # Создаем категории
        categories = [
            "Смартфоны",
            "Телевизоры",
            "Ноутбуки",
            "Планшеты",
            "Фотоаппараты",
            "Наушники",
            "Игровые консоли",
            "Умные часы",
            "Кухонная техника",
            "Пылесосы",
        ]
        for category in categories:
            Categories.objects.create(category=category)
        self.stdout.write(self.style.SUCCESS('10 Categories objects created'))

        # Создаем подкатегории и товары
        subcategories_data = {
            "Смартфоны": ["Apple", "Samsung", "Xiaomi"],
            "Телевизоры": ["LG", "Sony", "Samsung"],
            "Ноутбуки": ["Apple", "Asus", "Lenovo"],
            "Планшеты": ["Apple", "Samsung", "Huawei"],
            "Фотоаппараты": ["Canon", "Nikon", "Sony"],
            "Наушники": ["Sony", "JBL", "Apple"],
            "Игровые консоли": ["PlayStation", "Xbox", "Nintendo"],
            "Умные часы": ["Apple", "Samsung", "Huawei"],
            "Кухонная техника": ["Bosch", "Philips", "Tefal"],
            "Пылесосы": ["Dyson", "Samsung", "Xiaomi"],
        }

        products_data = {
            "Apple": [
                {"name": "iPhone 13", "price": 799, "description": "Новый iPhone 13", "photo_id": "iphone13"},
                {"name": "iPhone 14", "price": 999, "description": "Новый iPhone 14", "photo_id": "iphone14"},
                {"name": "MacBook Air", "price": 1299, "description": "Легкий и мощный", "photo_id": "macbook_air"},
                {"name": "iPad Pro", "price": 899, "description": "Мощный планшет", "photo_id": "ipad_pro"},
                {"name": "AirPods Pro", "price": 249, "description": "Беспроводные наушники",
                 "photo_id": "airpods_pro"},
            ],
            "Samsung": [
                {"name": "Galaxy S22", "price": 799, "description": "Флагман Samsung", "photo_id": "galaxy_s22"},
                {"name": "Galaxy Tab S8", "price": 699, "description": "Планшет Samsung", "photo_id": "galaxy_tab_s8"},
                {"name": "Galaxy Watch 4", "price": 299, "description": "Умные часы", "photo_id": "galaxy_watch_4"},
                {"name": "QLED TV", "price": 1499, "description": "Телевизор 4K", "photo_id": "qled_tv"},
                {"name": "Galaxy Buds", "price": 149, "description": "Беспроводные наушники",
                 "photo_id": "galaxy_buds"},
            ],
            # Добавьте данные для других подкатегорий
        }

        for category_name, subcategories in subcategories_data.items():
            category = Categories.objects.get(category=category_name)
            for subcategory_name in subcategories:
                subcategory = Subcategories.objects.create(name=subcategory_name, category=category)
                for product in products_data.get(subcategory_name, []):
                    Products.objects.create(
                        name=product["name"],
                        price=product["price"],
                        description=product["description"],
                        photo_id=product["photo_id"],
                        category=category,
                        subcategory=subcategory.name,
                    )
        self.stdout.write(self.style.SUCCESS('Subcategories and Products created'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
