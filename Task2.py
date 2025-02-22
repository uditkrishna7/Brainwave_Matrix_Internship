import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox

# Database Class
class Database:
    def __init__(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        # Ensure the inventory table exists with the correct schema
        self.cursor.execute("DROP TABLE IF EXISTS inventory")  # Ensures fresh schema
        self.cursor.execute('''
            CREATE TABLE inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_product(self, name, quantity, price):
        # Insert a new product into the inventory
        self.cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        self.conn.commit()

    def get_products(self):
        # Fetch all products from the inventory
        self.cursor.execute("SELECT * FROM inventory")
        return self.cursor.fetchall()

    def delete_product(self, product_id):
        # Delete a product based on its ID
        self.cursor.execute("DELETE FROM inventory WHERE id = ?", (product_id,))
        self.conn.commit()
    
    def update_product(self, product_id, name, quantity, price):
        # Update product details
        self.cursor.execute("UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?", 
                            (name, quantity, price, product_id))
        self.conn.commit()

# GUI Class
class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 600, 400)

        # Layout setup
        layout = QVBoxLayout()
        
        # Labels and Input Fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Product Name")
        layout.addWidget(self.name_input)
        
        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText("Quantity")
        layout.addWidget(self.quantity_input)
        
        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Price")
        layout.addWidget(self.price_input)
        
        # Buttons
        self.add_button = QPushButton("Add Product", self)
        self.add_button.clicked.connect(self.add_product)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Selected Product", self)
        self.update_button.clicked.connect(self.update_product)
        layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton("Delete Selected Product", self)
        self.delete_button.clicked.connect(self.delete_product)
        layout.addWidget(self.delete_button)
        
        # Table for displaying inventory
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Price"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.load_data()

    def add_product(self):
        # Add a new product
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        if not name or not quantity or not price:
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return
        
        try:
            self.db.add_product(name, int(quantity), float(price))
            self.load_data()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be an integer and price must be a number!")

    def load_data(self):
        # Load inventory data into the table
        self.table.setRowCount(0)
        for row_idx, (id, name, quantity, price) in enumerate(self.db.get_products()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(quantity)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(price)))
    
    def delete_product(self):
        # Delete selected product
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a product to delete!")
            return
        
        product_id = int(self.table.item(selected_row, 0).text())
        self.db.delete_product(product_id)
        self.load_data()
    
    def update_product(self):
        # Update selected product details
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a product to update!")
            return
        
        product_id = int(self.table.item(selected_row, 0).text())
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        
        if not name or not quantity or not price:
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return
        
        try:
            self.db.update_product(product_id, name, int(quantity), float(price))
            self.load_data()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be an integer and price must be a number!")

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
