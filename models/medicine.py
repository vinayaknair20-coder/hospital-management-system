from datetime import date
from validation.Pharmacist_validation import MedicineValidator

class Medicine:
    def __init__(self, medicine_id=None, medicine_name=None, generic_name=None,
                 medicine_type=None, manufacturer=None, batch_number=None,
                 quantity_in_stock=None, unitprice=None, expiry_date=None,
                 minimum_stock_level=None, is_active=None):

        self.__medicine_id = None
        self.__medicine_name = None
        self.__generic_name = None
        self.__medicine_type = None
        self.__manufacturer = None
        self.__batch_number = None
        self.__quantity_in_stock = None
        self.__unitprice = None
        self.__expiry_date = None
        self.__minimum_stock_level = None
        self.__is_active = is_active or '1'

        # Set values with validation if provided
        if medicine_id is not None:
            self.set_medicine_id(medicine_id)
        if medicine_name is not None:
            self.set_medicine_name(medicine_name)
        if generic_name is not None:
            self.set_gen_medicine_name(generic_name)
        if medicine_type is not None:
            self.set_medicine_type(medicine_type)
        if manufacturer is not None:
            self.set_manufacturer(manufacturer)
        if batch_number is not None:
            self.set_batch_number(batch_number)
        if quantity_in_stock is not None:
            self.set_quantity_in_stock(quantity_in_stock)
        if unitprice is not None:
            self.set_unit_price(unitprice)
        if expiry_date is not None:
            self.set_expiry_date(expiry_date)
        if minimum_stock_level is not None:
            self.set_minimum_stock_level(minimum_stock_level)

    def get_medicine_id(self):
        return self.__medicine_id

    def set_medicine_id(self, medicine_id):
        # Handle both string and int input
        if isinstance(medicine_id, str):
            is_valid, msg, val = MedicineValidator.validate_medicine_id(medicine_id)
            if not is_valid:
                raise ValueError(msg)
            medicine_id = val
        self.__medicine_id = int(medicine_id)

    def get_medicine_name(self):
        return self.__medicine_name

    def set_medicine_name(self, name):
        # Convert to string and validate
        name_str = str(name) if name is not None else ""
        is_valid, msg = MedicineValidator.validate_medicine_name(name_str)
        if not is_valid:
            raise ValueError(msg)
        self.__medicine_name = name_str.strip()

    def get_gen_medicine_name(self):
        return self.__generic_name

    def set_gen_medicine_name(self, name):
        # Convert to string and validate
        name_str = str(name) if name is not None else ""
        is_valid, msg = MedicineValidator.validate_medicine_name(name_str)
        if not is_valid:
            raise ValueError(msg)
        self.__generic_name = name_str.strip()

    def get_medicine_type(self):
        return self.__medicine_type

    def set_medicine_type(self, type_):
        # Convert to string and validate
        type_str = str(type_) if type_ is not None else ""
        is_valid, msg = MedicineValidator.validate_medicine_type(type_str)
        if not is_valid:
            raise ValueError(msg)
        self.__medicine_type = type_str.strip().title()

    def get_manufacturer(self):
        return self.__manufacturer

    def set_manufacturer(self, m):
        # Convert to string and validate
        m_str = str(m) if m is not None else ""
        is_valid, msg = MedicineValidator.validate_manufacturer(m_str)
        if not is_valid:
            raise ValueError(msg)
        self.__manufacturer = m_str.strip()

    def get_batch_number(self):
        return self.__batch_number

    def set_batch_number(self,batch_number):
    # More lenient validation - just convert to string
        self.__batch_number = str(batch_number)


    def get_quantity_in_stock(self):
        return self.__quantity_in_stock

    def set_quantity_in_stock(self, q):
        if isinstance(q, str):
            is_valid, msg, val = MedicineValidator.validate_quantity(q)
            if not is_valid:
                raise ValueError(msg)
            q = val
        self.__quantity_in_stock = int(q) if q is not None else 0

    def get_unit_price(self):
        return self.__unitprice

    def set_unit_price(self, p):
        if isinstance(p, str):
            is_valid, msg, val = MedicineValidator.validate_price(p)
            if not is_valid:
                raise ValueError(msg)
            p = val
        self.__unitprice = float(p) if p is not None else 0.0

    def get_expiry_date(self):
        return self.__expiry_date

    def set_expiry_date(self, edate):
        if isinstance(edate, str):
            is_valid, msg, val = MedicineValidator.validate_expiry_date(edate)
            if not is_valid:
                raise ValueError(msg)
            edate = val
        self.__expiry_date = edate

    def get_minimum_stock_level(self):
        return self.__minimum_stock_level

    def set_minimum_stock_level(self, msl):
        if isinstance(msl, str):
            is_valid, msg, val = MedicineValidator.validate_minimum_stock(msl, self.__quantity_in_stock)
            if not is_valid:
                raise ValueError(msg)
            msl = val
        self.__minimum_stock_level = int(msl) if msl is not None else 0

    def get_is_active(self):
        return self.__is_active

    def is_expired(self) -> bool:
        return self.__expiry_date and self.__expiry_date <= date.today()

    def is_critical_stock(self) -> bool:
        return self.__quantity_in_stock is not None and self.__quantity_in_stock <= 10

    def __str__(self):
        return (f"ID: {self.__medicine_id}, Name: {self.__medicine_name}, "
                f"Generic: {self.__generic_name}, Type: {self.__medicine_type}, Price: {self.__unitprice}, "
                f"Manufacturer: {self.__manufacturer}, Batch: {self.__batch_number}, "
                f"Stock: {self.__quantity_in_stock}, Expiry: {self.__expiry_date}, "
                f"Min Stock: {self.__minimum_stock_level}, Status: "
                f"{'Expired' if self.is_expired() else ('Critical Stock' if self.is_critical_stock() else 'Normal')}")
