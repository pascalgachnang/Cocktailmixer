import sqlite3

class DatabaseOrders:

    def __init__(self):
        #Connects to the database and creates the tables if they don't exist
        self.conn = sqlite3.connect('DatabaseOrders.db')
        self.curs = self.conn.cursor()
        self.create_table()

    def create_table(self):
        #Table for recipes
        self.curs.execute('''CREATE TABLE IF NOT EXISTS orders
             (id INTEGER PRIMARY KEY AUTOINCREMENT, recipe TEXT)''')
        
        #Table for ingredients
        self.curs.execute('''CREATE TABLE IF NOT EXISTS ingredients
             (id INTEGER PRIMARY KEY AUTOINCREMENT, ingredient TEXT)''')
        
        #Connection between orders and ingredients with the amount of each ingredient
        self.curs.execute('''CREATE TABLE IF NOT EXISTS order_ingredients
             (order_id INTEGER, ingredient_id INTEGER, amount REAL,
              FOREIGN KEY(order_id) REFERENCES orders(id),
              FOREIGN KEY(ingredient_id) REFERENCES ingredients(id))''')
        
        self.conn.commit()
    
    def insert_order(self, recipe, ingredients):
        #Inserts a new order into the database
        self.curs.execute("INSERT INTO orders (recipe) VALUES (?)", (recipe,))
        order_id = self.curs.lastrowid

        for ingredient in ingredients:
            #Inserts the ingredients into the database
            self.curs.execute("INSERT INTO ingredients (ingredient) VALUES (?)", (ingredient,))
            ingredient_id = self.curs.lastrowid
            #Inserts the connection between the order and the ingredients
            self.curs.execute("INSERT INTO order_ingredients (order_id, ingredient_id, amount) VALUES (?, ?, ?)", (order_id, ingredient_id, ingredients[ingredient]))
        self.conn.commit()

    def get_recipe_order_count(self):
        #Returns the amount of orders for each recipe
        self.curs.execute('''SELECT recipe, COUNT(*) as order_count 
                            FROM orders 
                            GROUP BY recipe''')
        return self.curs.fetchall()
    
    def get_total_ingredient_usage(self):
        #Returns the total amount of each ingredient used in all orders
        self.curs.execute('''SELECT i.ingredient, SUM(oi.amount) as total_amount
                            FROM order_ingredients oi
                            JOIN ingredients i ON oi.ingredient_id = i.id
                            GROUP BY i.ingredient''')
        return self.curs.fetchall()


    def show_orders(self):
                # Anzahl der Bestellungen pro Rezept abrufen
        print("Order count per recipe:")
        recipe_order_counts = self.get_recipe_order_count()
        for recipe, count in recipe_order_counts:
            print(f"Recipe: {recipe}, Orders: {count}")
        

        # Gesamtmenge jeder Zutat abrufen
        print("\nTotal ingredient usage:")
        total_ingredient_usage = self.get_total_ingredient_usage()
        for ingredient, total_amount in total_ingredient_usage:
            print(f"Ingredient: {ingredient}, Total Amount: {total_amount} cl")

