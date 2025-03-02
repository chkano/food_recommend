from datetime import datetime, timedelta
from typing import List, Tuple
import hashlib
import secrets
import random
import base64

class Customer:
    def __init__(self, customer_id: str, email: str, birthdate: datetime, gender: str, 
                 address: str, favorite_food: List[str] = None, password_hash: str = None, 
                 salt: str = None, last_login: datetime = None):
        self.customer_id = customer_id
        self.email = email
        self.birthdate = birthdate
        self.gender = gender
        self.address = address
        self.favorite_food = favorite_food if favorite_food is not None else []
        self.purchase_history = []
        self.password_hash = password_hash
        self.salt = salt
        self.last_login = last_login
    
    def set_password(self, password: str):
        """Set a new password with salt and hashing"""
        self.salt = secrets.token_hex(16)
        self.password_hash = self._hash_password(password, self.salt)
    
    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash"""
        if not self.password_hash or not self.salt:
            return False
        return self.password_hash == self._hash_password(password, self.salt)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash a password with the given salt"""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def record_login(self):
        """Record the current datetime as the last login time"""
        self.last_login = datetime.now()
    
    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "email": self.email,
            "birthdate": self.birthdate.isoformat(),
            "gender": self.gender,
            "address": self.address,
            "favorite_food": self.favorite_food,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            customer_id=data["customer_id"],
            email=data["email"],
            birthdate=datetime.fromisoformat(data["birthdate"]),
            gender=data["gender"],
            address=data["address"],
            favorite_food=data["favorite_food"],
            password_hash=data.get("password_hash"),
            salt=data.get("salt"),
            last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None
        )

class Receipt:
    def __init__(self, receipt_id: str, upload_date: datetime, image_data: bytes, 
                 ocr_text: str, ingredients: List[str], quantity: int, shelf_life: datetime):
        self.receipt_id = receipt_id
        self.upload_date = upload_date
        self.image_data = image_data
        self.ocr_text = ocr_text
        self.ingredients = ingredients
        self.quantity = quantity
        self.shelf_life = shelf_life
    
    def to_dict(self):
        return {
            "receipt_id": self.receipt_id,
            "upload_date": self.upload_date.isoformat(),
            "image_data": base64.b64encode(self.image_data).decode('utf-8') if self.image_data else None,
            "ocr_text": self.ocr_text,
            "ingredients": self.ingredients,
            "quantity": self.quantity,
            "shelf_life": self.shelf_life.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        image_data = base64.b64decode(data["image_data"]) if data.get("image_data") else None
        return cls(
            receipt_id=data["receipt_id"],
            upload_date=datetime.fromisoformat(data["upload_date"]),
            image_data=image_data,
            ocr_text=data["ocr_text"],
            ingredients=data["ingredients"],
            quantity=data["quantity"],
            shelf_life=datetime.fromisoformat(data["shelf_life"])
        )

class MenuItem:
    def __init__(self, item_id: str, name: str, ingredients: List[str], price: float):
        self.item_id = item_id
        self.name = name
        self.ingredients = ingredients
        self.price = price
    
    def match_ingredients(self, ingredients: List[str]) -> bool:
        return any(ingredient in self.ingredients for ingredient in ingredients)
    
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "ingredients": self.ingredients,
            "price": self.price
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data["item_id"],
            name=data["name"],
            ingredients=data["ingredients"],
            price=data["price"]
        )

class Store:
    def __init__(self, store_id: str, name: str, location: Tuple, menu_items: List[MenuItem]):
        self.store_id = store_id
        self.name = name
        self.location = location
        self.menu_items = menu_items
    
    def get_store_link(self) -> str:
        return f"https://www.example.com/store/{self.store_id}"
    
    def to_dict(self):
        return {
            "store_id": self.store_id,
            "name": self.name,
            "location": self.location,
            "menu_items": [item.to_dict() for item in self.menu_items]
        }
    
    @classmethod
    def from_dict(cls, data):
        menu_items = [MenuItem.from_dict(item) for item in data["menu_items"]]
        return cls(
            store_id=data["store_id"],
            name=data["name"],
            location=tuple(data["location"]),
            menu_items=menu_items
        )

class ReceiptSystem:
    def __init__(self):
        self.customers = []
        self.stores = []
        self.receipts = {}  # Map customer_id to list of receipts
        
    def register_customer(self, customer: Customer):
        """Register a new customer in the system"""
        # Check if customer already exists
        if any(c.customer_id == customer.customer_id for c in self.customers):
            raise ValueError(f"Customer with ID {customer.customer_id} already exists")
        
        if any(c.email == customer.email for c in self.customers):
            raise ValueError(f"Customer with email {customer.email} already exists")
            
        self.customers.append(customer)
        self.receipts[customer.customer_id] = []
        
    def add_store(self, store: Store):
        """Add a new store to the system"""
        if any(s.store_id == store.store_id for s in self.stores):
            raise ValueError(f"Store with ID {store.store_id} already exists")
            
        self.stores.append(store)
    
    def process_receipt(self, receipt: Receipt, customer_id=None):
        """
        Process a receipt by extracting text, identifying ingredients,
        and calculating shelf life
        """
        # Simulate OCR and ingredient extraction
        # In a real system, this would use actual OCR and NLP
        sample_ingredients = ["beef", "chicken", "lettuce", "tomato", 
                              "cheese", "bread", "milk", "eggs", "rice", "pasta"]
        
        # Randomly select 2-5 ingredients from the sample list
        num_ingredients = random.randint(2, 5)
        receipt.ingredients = random.sample(sample_ingredients, num_ingredients)
        
        # Generate some fake OCR text
        receipt.ocr_text = f"Receipt #{receipt.receipt_id}\n"
        receipt.ocr_text += f"Date: {receipt.upload_date.strftime('%Y-%m-%d')}\n"
        receipt.ocr_text += "Items:\n"
        for ingredient in receipt.ingredients:
            receipt.ocr_text += f"- {ingredient.capitalize()} ${random.uniform(1.99, 15.99):.2f}\n"
        
        # Calculate shelf life based on ingredients (simplified)
        # In a real system, this would use a more sophisticated algorithm
        shelf_life_days = 7  # Default shelf life is 7 days
        if "milk" in receipt.ingredients or "eggs" in receipt.ingredients:
            shelf_life_days = 3  # Dairy products have shorter shelf life
        
        receipt.shelf_life = receipt.upload_date + timedelta(days=shelf_life_days)
        
        # Associate receipt with customer if provided
        if customer_id and customer_id in self.receipts:
            self.receipts[customer_id].append(receipt)
        
    def get_recommendations(self, customer: Customer) -> List[MenuItem]:
        """
        Generate personalized recommendations for a customer based on
        their purchase history, preferences, and item shelf life
        """
        all_menu_items = []
        for store in self.stores:
            all_menu_items.extend(store.menu_items)
            
        if not all_menu_items:
            return []
        
        # Get customer's receipts and extract all ingredients
        customer_ingredients = set(customer.favorite_food)
        if customer.customer_id in self.receipts:
            for receipt in self.receipts[customer.customer_id]:
                customer_ingredients.update(receipt.ingredients)
        
        # Find menu items that match the customer's ingredients
        matching_items = []
        for item in all_menu_items:
            if any(ingredient in item.ingredients for ingredient in customer_ingredients):
                matching_items.append(item)
        
        if matching_items:
            # Return up to 3 matching items, prioritizing those with more matching ingredients
            matching_items.sort(key=lambda x: sum(1 for ing in customer_ingredients if ing in x.ingredients), reverse=True)
            return matching_items[:3]
        else:
            # If no matches found, return random items
            num_recommendations = min(len(all_menu_items), random.randint(1, 3))
            return random.sample(all_menu_items, num_recommendations)
    
    # Add authentication methods
    def authenticate_customer(self, email: str, password: str) -> Customer:
        """Authenticate a customer by email and password"""
        customer = self.get_customer_by_email(email)
        if not customer:
            return None
        
        if customer.verify_password(password):
            customer.record_login()
            return customer
        return None
    
    def get_customer_by_email(self, email: str) -> Customer:
        """Get a customer by their email address"""
        for customer in self.customers:
            if customer.email.lower() == email.lower():
                return customer
        return None
    
    def update_customer(self, customer: Customer) -> bool:
        """Update an existing customer in the system"""
        for i, c in enumerate(self.customers):
            if c.customer_id == customer.customer_id:
                self.customers[i] = customer
                return True
        return False
    
    def to_dict(self):
        return {
            "customers": [c.to_dict() for c in self.customers],
            "stores": [s.to_dict() for s in self.stores],
            "receipts": {
                customer_id: [r.to_dict() for r in receipts] 
                for customer_id, receipts in self.receipts.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        system = cls()
        
        # Load stores first
        for store_data in data.get("stores", []):
            store = Store.from_dict(store_data)
            system.stores.append(store)
        
        # Load customers
        for customer_data in data.get("customers", []):
            customer = Customer.from_dict(customer_data)
            system.customers.append(customer)
        
        # Load receipts
        for customer_id, receipts_data in data.get("receipts", {}).items():
            system.receipts[customer_id] = [Receipt.from_dict(r) for r in receipts_data]
        
        return system