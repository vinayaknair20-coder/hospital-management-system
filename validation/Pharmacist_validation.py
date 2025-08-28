import re
from datetime import datetime, date
from typing import Optional, Tuple, List

class MedicineValidator:
    NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9\s_-]{1,49}$")
    MANUFACTURER_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9\s&.,'-]{1,49}$")
    BATCH_PATTERN = re.compile(r"^[A-Za-z0-9]{3,20}$")
    MEDICINE_TYPES = [
        "Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drop", "Inhaler", "Patch",
        "Powder", "Cream", "Gel", "Lotion", "Spray", "Suppository", "Other"
    ]
    CRITICAL_STOCK_LEVEL = 10

    @staticmethod
    def validate_medicine_id(medicine_id: str) -> Tuple[bool, str, Optional[int]]:
        try:
            if not medicine_id.strip():
                return False, "Medicine ID cannot be empty", None
            med_id = int(medicine_id)
            if med_id <= 0:
                return False, "Medicine ID must be a positive number", None
            if med_id > 999999:
                return False, "Medicine ID cannot exceed 6 digits", None
            return True, "Valid", med_id
        except ValueError:
            return False, "Medicine ID must be a valid number", None

    @staticmethod
    def validate_medicine_name(name: str) -> Tuple[bool, str]:
        name = (name or "").strip()
        if len(name) < 2:
            return False, "Medicine name must be at least 2 characters"
        if len(name) > 50:
            return False, "Medicine name cannot exceed 50 characters"
        if not MedicineValidator.NAME_PATTERN.match(name):
            return False, "Invalid medicine name"
        return True, "Valid"

    @staticmethod
    def validate_medicine_type(medicine_type: str) -> Tuple[bool, str]:
        medicine_type = (medicine_type or "").strip().title()
        if medicine_type not in MedicineValidator.MEDICINE_TYPES:
            return False, f"Invalid type. Must be one of: {', '.join(MedicineValidator.MEDICINE_TYPES)}"
        return True, "Valid"

    @staticmethod
    def get_medicine_types() -> List[str]:
        return MedicineValidator.MEDICINE_TYPES.copy()

    @staticmethod
    def validate_manufacturer(manufacturer: str) -> Tuple[bool, str]:
        manufacturer = (manufacturer or "").strip()
        if len(manufacturer) < 2:
            return False, "Manufacturer must be at least 2 characters"
        if len(manufacturer) > 50:
            return False, "Manufacturer cannot exceed 50 characters"
        if not MedicineValidator.MANUFACTURER_PATTERN.match(manufacturer):
            return False, "Invalid manufacturer name"
        return True, "Valid"

    @staticmethod
    def validate_batch_number(batch: str) -> Tuple[bool, str]:
        batch = (batch or "").strip().upper()
        if not MedicineValidator.BATCH_PATTERN.match(batch):
            return False, "Batch number must be 3-20 alphanumeric"
        return True, "Valid"

    @staticmethod
    def validate_quantity(quantity: str) -> Tuple[bool, str, Optional[int]]:
        try:
            qty = int(quantity)
            if qty < 0:
                return False, "Quantity cannot be negative", None
            if qty > 10000:
                return False, "Quantity seems unusually high (max: 10,000)", None
            return True, "Valid", qty
        except ValueError:
            return False, "Quantity must be a valid number", None

    @staticmethod
    def validate_price(price: str) -> Tuple[bool, str, Optional[float]]:
        try:
            unit_price = float(price)
            if unit_price < 0:
                return False, "Price cannot be negative", None
            if unit_price > 100000:
                return False, "Price seems unusually high (max: 100,000)", None
            return True, "Valid", round(unit_price, 2)
        except ValueError:
            return False, "Price must be a valid number", None

    @staticmethod
    def validate_expiry_date(date_str: str) -> Tuple[bool, str, Optional[date]]:
        if not date_str.strip():
            return False, "Expiry date cannot be empty", None
        for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']:
            try:
                parsed_date = datetime.strptime(date_str.strip(), fmt).date()
                today = date.today()
                if parsed_date <= today:
                    return False, "Expiry date must be in the future", None
                if parsed_date > date(today.year+10, today.month, today.day):
                    return False, "Expiry too far in future (max 10 years)", None
                return True, "Valid", parsed_date
            except ValueError:
                continue
        return False, "Invalid date format. Use DD/MM/YYYY", None

    @staticmethod
    def validate_minimum_stock(stock_str: str, current_stock: Optional[int] = None) -> Tuple[bool, str, Optional[int]]:
        try:
            min_stock = int(stock_str)
            if min_stock < 0:
                return False, "Minimum stock cannot be negative", None
            if min_stock > 1000:
                return False, "Minimum stock seems unusually high (max: 1,000)", None
            if current_stock is not None and min_stock > current_stock:
                return False, f"Minimum stock ({min_stock}) cannot be higher than current stock ({current_stock})", None
            return True, "Valid", min_stock
        except ValueError:
            return False, "Minimum stock must be a valid number", None

    @staticmethod
    def check_stock_level(quantity: int) -> dict:
        cl = MedicineValidator.CRITICAL_STOCK_LEVEL
        if quantity <= cl:
            return {"level": "CRITICAL", "alert": True}
        else:
            return {"level": "NORMAL", "alert": False}

class InputValidator:
    @staticmethod
    def get_validated_input(prompt: str, validator_func, max_attempts: int = 3):
        for _ in range(max_attempts):
            try:
                user_input = input(f"{prompt}: ").strip()
                result = validator_func(user_input)
                if result[0]:
                    return result[-1] if len(result) > 2 else user_input
                else:
                    print(f"[!] {result[1]}")
            except KeyboardInterrupt:
                print("[x] Operation cancelled")
                return None
        print("[x] Operation aborted.")
        return None

    @staticmethod
    def get_medicine_type_choice():
        types = MedicineValidator.get_medicine_types()
        print("Available Medicine Types:")
        for i, med_type in enumerate(types, 1):
            print(f"{i}. {med_type}")
        while True:
            choice = input(f"Select medicine type (1-{len(types)}): ").strip()
            try:
                c = int(choice)
                if 1 <= c <= len(types):
                    return types[c-1]
                else:
                    print("[!] Enter a number from the list.")
            except ValueError:
                print("[!] Invalid entry.")

    @staticmethod
    def confirm_action(message: str) -> bool:
        while True:
            resp = input(f"{message} (y/n): ").strip().lower()
            if resp in ["y", "yes"]:
                return True
            if resp in ["n", "no"]:
                return False
            print("[!] Enter 'y' or 'n'.")
