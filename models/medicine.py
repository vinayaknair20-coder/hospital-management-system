from datetime import date
import re

class Medicine:
    """Python OOPs applied for Medicine management"""
    
    def _init_(self, medicine_id=None, medicine_name=None,generic_name=None,manufacturer=None,batch_number=None,quantity_in_stock=None,unitprice=None,expiry_date=None,minimum_stock_level=None, is_active=None):
        self.__medicine_id = medicine_id
        self.__medicine_name = medicine_name
        self.__generic_name = generic_name
        self.__manufacturer = manufacturer
        self.batch_number = batch_number
        self.__quantity_in_stock = quantity_in_stock
        self.__unitprice = unitprice
        self.__expiry_date = expiry_date
        self.__minimum_stock_level = minimum_stock_level
        self.__is_active = is_active

    # Getters and Setters
    def get_medicine_id(self):
        return self.__medicine_id
    
    def set_medicine_id(self, medicine_id):
        self.__medicine_id = medicine_id

    def get_medicine_name(self):
        return self.__medicine_name
    
    def set_medicine_name(self, medicine_name):
        """Validate medicine name (2-30 alphabets/underscore only)"""
        pattern = re.compile(r"^[A-Za-z_]{2,30}$")
        
        if pattern.match(medicine_name):
            self.__medicineame = medicineName
        else:
            raise ValueError("Invalid medicine name: must contain only alphabets and underscores, length 2-30 characters")

    def get_price(self):
        return self.__price
    
    def set_price(self, price):
        if price is not None and price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price

    def get_manufacture_date(self):
        return self.__manufacturedate

    def set_manufacture_date(self, manufacturedate):
        if isinstance(manufacturedate, date):
            self.__manufacturedate = manufacturedate
        else:
            raise ValueError("Manufacture date must be a date object")

    def _str_(self):
        return f"Medicine ID: {self._medicineid:<10}, Medicine Name: {self.medicineName:<15}, Price: {self.price:<10}, Manufacture Date: {self._manufacturedate}"
