from validation.Pharmacist_validation import PharmacyValidator
from typing import Union, Optional
from datetime import date

class InputHelper:
    """
    Helper class for getting validated inputs with retry mechanism
    """
    
    @staticmethod
    def get_validated_input(prompt: str, validator_func, max_attempts: int = 3):
        """
        Generic method to get validated input with retry mechanism
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                user_input = input(prompt).strip()
                result = validator_func(user_input)
                
                if result[0]:  # If validation passed
                    if len(result) > 2:  # Has additional data (like parsed date)
                        return result[2] if result[2] is not None else user_input
                    return user_input
                else:
                    print(f"Error: {result[1]}")
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"Please try again ({max_attempts - attempts} attempts remaining)")
            
            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                return None
            except Exception as e:
                print(f"Unexpected error: {e}")
                attempts += 1
        
        print(f"Maximum attempts ({max_attempts}) reached. Operation cancelled.")
        return None
    
    @staticmethod
    def get_medicine_id(prompt: str = "Enter medicine ID: ") -> Optional[int]:
        """Get validated medicine ID"""
        result = InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_medicine_id
        )
        return int(result) if result is not None else None
    
    @staticmethod
    def get_medicine_name(prompt: str = "Enter medicine name: ") -> Optional[str]:
        """Get validated medicine name"""
        return InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_medicine_name
        )
    
    @staticmethod
    def get_generic_name(prompt: str = "Enter generic name: ") -> Optional[str]:
        """Get validated generic name"""
        return InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_generic_name
        )
    
    @staticmethod
    def get_manufacturer(prompt: str = "Enter manufacturer: ") -> Optional[str]:
        """Get validated manufacturer"""
        return InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_manufacturer
        )
    
    @staticmethod
    def get_batch_number(prompt: str = "Enter batch number: ") -> Optional[str]:
        """Get validated batch number"""
        return InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_batch_number
        )
    
    @staticmethod
    def get_quantity(prompt: str = "Enter quantity in stock: ") -> Optional[int]:
        """Get validated quantity"""
        result = InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_quantity
        )
        return int(result) if result is not None else None
    
    @staticmethod
    def get_unit_price(prompt: str = "Enter unit price: ") -> Optional[float]:
        """Get validated unit price"""
        result = InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_unit_price
        )
        return float(result) if result is not None else None
    
    @staticmethod
    def get_expiry_date(prompt: str = "Enter expiry date (dd/mm/yyyy): ") -> Optional[date]:
        """Get validated expiry date"""
        return InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_expiry_date
        )
    
    @staticmethod
    def get_minimum_stock_level(prompt: str = "Enter minimum stock level: ") -> Optional[int]:
        """Get validated minimum stock level"""
        result = InputHelper.get_validated_input(
            prompt, 
            PharmacyValidator.validate_minimum_stock_level
        )
        return int(result) if result is not None else None
    
    @staticmethod
    def get_confirmation(prompt: str = "Do you want to continue? (y/n): ") -> Optional[bool]:
        """Get validated confirmation"""
        result = InputHelper.get_validated_input(
            prompt, 
            lambda x: PharmacyValidator.validate_confirmation_input(x)
        )
        return result
    
    @staticmethod
    def get_menu_choice(prompt: str, max_option: int) -> Optional[int]:
        """Get validated menu choice"""
        result = InputHelper.get_validated_input(
            prompt, 
            lambda x: PharmacyValidator.validate_menu_choice(x, max_option)
        )
        return int(result) if result is not None else None
