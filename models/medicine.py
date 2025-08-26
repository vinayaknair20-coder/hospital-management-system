from datetime import date,datetime
import re

class Medicine:
    """Python OOPs applied for Medicine management"""
    
    def _init_(self, medicine_id=None, medicine_name=None,generic_name=None,manufacturer=None,batch_number=None,quantity_in_stock=None,unitprice=None,expiry_date=None,minimum_stock_level=None, is_active=None):
        self.__medicine_id = medicine_id
        self.__medicine_name = medicine_name
        self.__generic_name = generic_name
        self.__manufacturer = manufacturer
        self.__batch_number = batch_number
        self.__quantity_in_stock = quantity_in_stock
        self.__unitprice = unitprice
        self.__expiry_date = expiry_date or datetime.now()
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
            self.__medicineame = medicine_name
        else:
            raise ValueError("Invalid medicine name: must contain only alphabets and underscores, length 2-30 characters")
        
    
    def get_gen_medicine_name(self):
        return self.__generic_name
    
    def set_gen_medicine_name(self, generic_name):
        """Validate medicine name (2-30 alphabets/underscore only)"""
        pattern = re.compile(r"^[A-Za-z_]{2,30}$")
        
        if pattern.match(generic_name):
            self.__generic_name = generic_name
        else:
            raise ValueError("Invalid medicine name: must contain only alphabets and underscores, length 2-30 characters")

    def get_unit_price(self):
        return self.__unitprice
    
    def set_price(self, unitprice):
        if unitprice is not None and unitprice < 0:
            raise ValueError("Price cannot be negative")
        self.__unitprice = unitprice

    def get_manufacturer(self):
        return self.__manufacturer

    def set_manufacturer(self, manufacturer):
        pattern = re.compile(r"^[A-Za-z_]{2,30}$")
        
        if pattern.match(manufacturer):
            self.__manufacturer = manufacturer
        else:
            raise ValueError("Invalid manufacturer: must contain only alphabets and underscores, length 2-30 characters")
    
    def get_batch_number(self):
        return self.__batch_number
    
    def set_batch_number(self,batch_number):
        self.__batch_number = batch_number

    def get_quantity_in_stock(self):
        return self.__quantity_in_stock
    
    def set_quantity_in_stock(self,quantity_in_stock):
        self.__quantity_in_stock = quantity_in_stock

    def get_expiry_date(self):
        return self.__expiry_date
    
    def set_expiry_date(self,expiry_date):
        self.__expiry_date = expiry_date

    def get_minimum_stock_level(self):
        return self.__minimum_stock_level
    
    def set_minimum_stock_level(self,minimum_stock_level):
        self.__minimum_stock_level = minimum_stock_level

    def get_is_active(self):
        return self.__is_active
    
    def set_is_active(self,is_active):
        self.__is_active = is_active

    def _str_(self):
        return f"Medicine ID: {self.__medicine_id:<10}, Medicine Name: {self.__medicine_name:<15},Generic Name:{self.__generic_name} Price: {self.__unitprice:<10}, Manufactu: {self.__manufacturer},batch_number:{self.__batch_number},quantity_in_stock:{self.__quantity_in_stock},expiry_date:{self.__expiry_date},minimum_stock_level:{self.__minimum_stock_level},is_active:{self.__is_active}"
