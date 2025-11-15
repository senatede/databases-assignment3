import os
import random
import pandas as pd
import datetime
from faker import Faker

OUT_DIR = "./generated_data"
os.makedirs(OUT_DIR, exist_ok=True)

fake = Faker()

def maybe_none(value, prob=0.1):
    return None if random.random() < prob else value

def gen_random_timestamp(start_date, end_date):
    time_diff = end_date - start_date
    random_seconds = random.randint(0, int(time_diff.total_seconds()))
    return start_date + datetime.timedelta(seconds=random_seconds)


def gen_restaurants(n=100):
    CITIES_REGIONS = {
        'Kyiv': 'Kyiv',
        'Lviv': 'Lviv',
        'Odesa': 'Odesa',
        'Kharkiv': 'Kharkiv',
        'Dnipro': 'Dnipropetrovsk',
        'Vinnytsia': 'Vinnytsia',
        'Lutsk': 'Volyn'
    }
    STREET_NAMES = [
        'Shevchenka Ave', 'Khreshchatyk St', 'Sobornosti Ave',
        'Haharina Ave', 'Derybasivska St', 'Svobody Ave',
        'Khmelnytske Hwy', 'Stepana Bandery St'
    ]

    rows = []
    for i in range(1, n + 1):
        city = random.choice(list(CITIES_REGIONS.keys()))
        street = random.choice(STREET_NAMES)
        street_num = random.randint(1, 150)

        rows.append({
            "restaurant_id": f"rest_{i:03d}",
            "address": maybe_none(f"{street} {street_num}"),
            "city": maybe_none(city),
            "region": maybe_none(CITIES_REGIONS[city])
        })

    df = pd.DataFrame(rows)
    df = pd.concat([df, df.sample(frac=0.1)], ignore_index=True)
    file = os.path.join(OUT_DIR, "raw_restaurants.csv")
    df.to_csv(file, index=False)

    print(f"Generated {len(df)} restaurants records -> {file}")
    return df

def gen_menu_items():
    MENU_ITEMS = [
        # Burgers (8)
        ('Big Mac', 'Burger', 75.00),
        ('Cheeseburger', 'Burger', 42.50),
        ('Hamburger', 'Burger', 38.00),
        ('Double Cheeseburger', 'Burger', 65.00),
        ('McChicken', 'Burger', 70.00),
        ('Filet-O-Fish', 'Chicken & Fish', 68.00),
        ('Quarter Pounder', 'Burger', 80.00),
        ('Big Tasty', 'Burger', 110.00),

        # Chicken (5)
        ('Chicken McNuggets (6)', 'Chicken & Fish', 90.00),
        ('Chicken McNuggets (9)', 'Chicken & Fish', 125.00),
        ('Chicken McNuggets (20)', 'Chicken & Fish', 240.00),
        ('Spicy Chicken Burger', 'Chicken & Fish', 72.00),
        ('Chicken Wrap', 'Chicken & Fish', 85.00),

        # Sides (5)
        ('Fries (Large)', 'Side', 40.00),
        ('Fries (Medium)', 'Side', 35.00),
        ('Fries (Small)', 'Side', 28.00),
        ('Potato Wedges', 'Side', 45.00),
        ('Onion Rings', 'Side', 50.00),

        # Salads (3)
        ('Garden Salad', 'Salad', 65.00),
        ('Caesar Salad', 'Salad', 85.00),
        ('Caesar Salad with Chicken', 'Salad', 105.00),

        # Cold Drinks (8)
        ('Coca-Cola (Large)', 'Drink (Cold)', 35.00),
        ('Coca-Cola (Medium)', 'Drink (Cold)', 32.50),
        ('Coca-Cola (Small)', 'Drink (Cold)', 30.00),
        ('Sprite (Medium)', 'Drink (Cold)', 32.50),
        ('Fanta (Medium)', 'Drink (Cold)', 32.50),
        ('Orange Juice', 'Drink (Cold)', 45.00),
        ('Still Water', 'Drink (Cold)', 25.00),
        ('Iced Latte', 'Drink (Cold)', 55.00),

        # Hot Drinks (6)
        ('Espresso', 'Drink (Hot)', 30.00),
        ('Americano', 'Drink (Hot)', 35.00),
        ('Cappuccino', 'Drink (Hot)', 45.00),
        ('Latte', 'Drink (Hot)', 50.00),
        ('Hot Tea (Black)', 'Drink (Hot)', 25.00),
        ('Hot Chocolate', 'Drink (Hot)', 50.00),

        # Desserts (6)
        ('McFlurry', 'Dessert', 60.00),
        ('Apple Pie', 'Dessert', 45.00),
        ('Sundae (Chocolate)', 'Dessert', 50.00),
        ('Sundae (Caramel)', 'Dessert', 50.00),
        ('Ice Cream Cone', 'Dessert', 25.00),
        ('Donut', 'Dessert', 35.00),

        # Breakfast (5)
        ('Egg McMuffin', 'Breakfast', 60.00),
        ('Sausage McMuffin', 'Breakfast', 65.00),
        ('Hash Brown', 'Breakfast', 30.00),
        ('Pancakes (3)', 'Breakfast', 70.00),
        ('Breakfast Wrap', 'Breakfast', 75.00),

        # McCafe Bakery (3)
        ('Croissant', 'McCafe', 40.00),
        ('Chocolate Chip Cookie', 'McCafe', 30.00),
        ('Blueberry Muffin', 'McCafe', 55.00),

        # Kids (1)
        ('Happy Meal', 'Kids', 130.00)
    ]

    rows = []
    for i, item in enumerate(MENU_ITEMS):
        name, category, unit_cost = item
        rows.append({
            "product_id": f"prod_{i + 1:03d}",
            "name": name,
            "category": category,
            "unit_cost": f"{unit_cost:.2f}"
        })
    df = pd.DataFrame(rows)
    df = pd.concat([df, df.sample(frac=0.1)], ignore_index=True)
    file = os.path.join(OUT_DIR, "raw_menu_items.csv")
    df.to_csv(file, index=False)

    print(f"Generated {len(df)} restaurants records -> {file}")
    return df

def gen_transactions(n, restaurants_df, menu_df):
    restaurant_ids = restaurants_df["restaurant_id"].unique().tolist()

    menu_lookup = {}
    for _, row in menu_df.iterrows():
        unit_cost = float(row['unit_cost'])
        list_price = unit_cost * (1 + random.uniform(0.7, 1.0)) # 70-100% markup
        menu_lookup[row['product_id']] = {
            'cost': unit_cost,
            'price': list_price
        }

    product_ids = list(menu_lookup.keys())

    start_date = datetime.datetime(2025, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2025, 12, 31, 23, 59, 59)

    transactions_rows = []
    transaction_items_rows = []

    for order_id_counter in range(1, n + 1):
        order_id = f"ord_{order_id_counter:06d}"

        order_timestamp = gen_random_timestamp(start_date, end_date)
        restaurant_id = random.choice(restaurant_ids)

        transactions_rows.append({
            "order_id": order_id,
            "timestamp": maybe_none(order_timestamp.isoformat()),
            "restaurant_id": maybe_none(restaurant_id, 0.05)
        })

        num_items_in_order = random.randint(1, 6)
        for _ in range(num_items_in_order):
            product_id = random.choice(product_ids)
            # Most orders are for 1 item
            quantity = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05], k=1)[0]
            item_info = menu_lookup[product_id]
            base_price = item_info['price'] * quantity

            # 10% chance of a 20% discount (promo)
            if random.random() < 0.1:
                final_price = base_price * 0.80
            else:
                final_price = base_price

            transaction_items_rows.append({
                "order_id": maybe_none(order_id, 0.05),
                "product_id": maybe_none(product_id, 0.05),
                "quantity":  maybe_none(f"{quantity}", 0.05),
                "price": maybe_none(f"{final_price:.2f}", 0.05)
            })

    trans_df = pd.DataFrame(transactions_rows)
    items_df = pd.DataFrame(transaction_items_rows)

    trans_df = pd.concat([trans_df, trans_df.sample(frac=0.05)], ignore_index=True)
    items_df = pd.concat([items_df, items_df.sample(frac=0.05)], ignore_index=True)

    trans_file = os.path.join(OUT_DIR, "raw_transactions.csv")
    items_file = os.path.join(OUT_DIR, "raw_transaction_items.csv")

    trans_df.to_csv(trans_file, index=False)
    items_df.to_csv(items_file, index=False)

    print(f"Generated {len(trans_df)} transaction records -> {trans_file}")
    print(f"Generated {len(items_df)} transaction_item records -> {items_file}")
    return trans_df, items_df

if __name__ == "__main__":
    print("Generating dirty CSV data in", OUT_DIR)
    restaurants = gen_restaurants(100)
    menu_items = gen_menu_items()
    gen_transactions(10000, restaurants, menu_items)
    print("All CSV files generated.")