from dao.absatractDaoPharma import MedecineDaoService
from dao.pharmaDaoImp import MedicineDaoImp
from models.medicine import Medicine
from validation.Pharmacist_validation import MedicineValidator, InputValidator
from datetime import date

class MedicineManagementLib:
    dao_service: MedecineDaoService = MedicineDaoImp()

    @staticmethod
    def display_medicine():
        try:
            print("\n" + "="*80)
            print("MEDICINE INVENTORY".center(80))
            print("="*80)
            medicines = MedicineManagementLib.dao_service.display_all_medicine()
            if not medicines:
                print("No medicines found in inventory")
                return
            critical_count = sum(1 for med in medicines if med.is_critical_stock())
            if critical_count > 0:
                print(f"\nStock alert: {critical_count} medicines at or below 10 units (critical level)")
                print("-"*80)
            medicine_types = {}
            for medicine in medicines:
                med_type = medicine.get_medicine_type()
                medicine_types.setdefault(med_type, []).append(medicine)
            for med_type, type_meds in medicine_types.items():
                print(f"\n{med_type.upper()} ({len(type_meds)}):")
                print("-"*80)
                for i, medicine in enumerate(type_meds, 1):
                    print(f"{i}. {medicine}")
                    if medicine.is_expired():
                        print("   [!] This medicine has expired.")
                    elif medicine.is_critical_stock():
                        print(f"   [!] Critical stock: {medicine.get_quantity_in_stock()} units.")
            print(f"\nTotal medicines: {len(medicines)}")
        except Exception as e:
            print(f"Error displaying medicines: {e}")

    @staticmethod
    def insert_medicine():
        try:
            print("\n" + "="*60)
            print("ADD NEW MEDICINE".center(60))
            print("="*60)
            medicine = Medicine()
            medicine_id = InputValidator.get_validated_input("Enter Medicine ID (numeric)", MedicineValidator.validate_medicine_id)
            if medicine_id is None: print("Operation cancelled"); return
            if MedicineManagementLib.dao_service.find_by_medicine_id(medicine_id):
                print("Medicine with this ID already exists."); return
            medicine.set_medicine_id(medicine_id)
            medicine_name = InputValidator.get_validated_input("Enter Medicine Name", MedicineValidator.validate_medicine_name)
            if medicine_name is None: return
            medicine.set_medicine_name(medicine_name)
            generic_name = InputValidator.get_validated_input("Enter Generic Name", MedicineValidator.validate_medicine_name)
            if generic_name is None: return
            medicine.set_gen_medicine_name(generic_name)
            medicine_type = InputValidator.get_medicine_type_choice()
            if medicine_type is None: return
            medicine.set_medicine_type(medicine_type)
            manufacturer = InputValidator.get_validated_input("Enter Manufacturer", MedicineValidator.validate_manufacturer)
            if manufacturer is None: return
            medicine.set_manufacturer(manufacturer)
            batch_number = InputValidator.get_validated_input("Enter Batch Number", MedicineValidator.validate_batch_number)
            if batch_number is None: return
            medicine.set_batch_number(batch_number)
            quantity = InputValidator.get_validated_input("Enter Quantity in Stock", MedicineValidator.validate_quantity)
            if quantity is None: return
            medicine.set_quantity_in_stock(quantity)
            unit_price = InputValidator.get_validated_input("Enter Unit Price", MedicineValidator.validate_price)
            if unit_price is None: return
            medicine.set_unit_price(unit_price)
            expiry_date = InputValidator.get_validated_input("Enter Expiry Date (DD/MM/YYYY)", MedicineValidator.validate_expiry_date)
            if expiry_date is None: return
            medicine.set_expiry_date(expiry_date)
            min_stock = InputValidator.get_validated_input("Enter Minimum Stock Level", lambda x: MedicineValidator.validate_minimum_stock(x, quantity))
            if min_stock is None: return
            medicine.set_minimum_stock_level(min_stock)
            print("\nMedicine details summary:")
            print(medicine)
            if not InputValidator.confirm_action("Confirm to save this medicine?"):
                print("Add cancelled."); return
            if MedicineManagementLib.dao_service.add_medicine(medicine):
                print("Medicine added successfully.")
                if medicine.is_critical_stock():
                    print("This medicine is at critical stock level.")
            else:
                print("Failed to add medicine.")
        except Exception as e:
            print(f"Error adding medicine: {e}")

    @staticmethod

    def update_medicine():
        try:
            print("\n" + "="*60)
            print("UPDATE MEDICINE".center(60))
            print("="*60)
            
            search_id = InputValidator.get_validated_input("Enter Medicine ID to update", MedicineValidator.validate_medicine_id)
            if search_id is None: return

            medicine = MedicineManagementLib.dao_service.find_by_medicine_id(search_id)
            if not medicine:
                print("Medicine not found"); return

            print("\nCurrent Medicine Details:")
            print(medicine)
            if medicine.is_expired():
                print("[!] Medicine is expired.")
            if medicine.is_critical_stock():
                print("[!] Medicine is at critical stock level.")

            if not InputValidator.confirm_action("Update this medicine?"):
                print("Update cancelled."); return

            # Update medicine name
            new_name = InputValidator.get_validated_input("New name (Enter to keep current)", lambda x: (True, "") if x == "" else MedicineValidator.validate_medicine_name(x))
            if new_name: medicine.set_medicine_name(new_name)

            # Update medicine type
            update_type = input("Change medicine type? (y/n): ").strip().lower()
            if update_type == 'y':
                new_type = InputValidator.get_medicine_type_choice()
                if new_type: medicine.set_medicine_type(new_type)

            # Update unit price
            new_price = InputValidator.get_validated_input("New unit price (Enter to keep current)", lambda x: (True, "", None) if x == "" else MedicineValidator.validate_price(x))
            if new_price: medicine.set_unit_price(new_price)

            # UPDATE STOCK/QUANTITY - NEW FEATURE
            update_stock = input("Update stock quantity? (y/n): ").strip().lower()
            if update_stock == 'y':
                current_stock = medicine.get_quantity_in_stock()
                print(f"Current stock: {current_stock}")
                
                stock_action = input("Choose: (1) Set new stock (2) Add to stock (3) Reduce stock: ").strip()
                
                if stock_action == "1":
                    # Set new stock
                    new_stock = InputValidator.get_validated_input("Enter new stock quantity", MedicineValidator.validate_quantity)
                    if new_stock is not None: 
                        medicine.set_quantity_in_stock(new_stock)
                        print(f"Stock updated from {current_stock} to {new_stock}")
                
                elif stock_action == "2":
                    # Add to stock
                    add_qty = InputValidator.get_validated_input("Enter quantity to add", MedicineValidator.validate_quantity)
                    if add_qty is not None:
                        new_total = current_stock + add_qty
                        medicine.set_quantity_in_stock(new_total)
                        print(f"Added {add_qty} units. Stock updated from {current_stock} to {new_total}")
                
                elif stock_action == "3":
                    # Reduce stock
                    reduce_qty = InputValidator.get_validated_input("Enter quantity to reduce", MedicineValidator.validate_quantity)
                    if reduce_qty is not None:
                        if reduce_qty <= current_stock:
                            new_total = current_stock - reduce_qty
                            medicine.set_quantity_in_stock(new_total)
                            print(f"Reduced {reduce_qty} units. Stock updated from {current_stock} to {new_total}")
                        else:
                            print("Cannot reduce more than current stock!")

            print("Updated medicine details:")
            print(medicine)

            if not InputValidator.confirm_action("Save these changes?"):
                print("Update cancelled."); return

            if MedicineManagementLib.dao_service.update_medicine(medicine, search_id):
                print("Medicine updated successfully.")
                updated = MedicineManagementLib.dao_service.find_by_medicine_id(search_id)
                if updated and updated.is_critical_stock():
                    print("Warning: Medicine now at critical stock level.")
            else:
                print("Failed to update medicine.")

        except Exception as e:
            print(f"Error updating medicine: {e}")


    @staticmethod
    def disable_medicine():
        try:
            print("\n" + "="*60)
            print("DISABLE MEDICINE".center(60))
            print("="*60)
            search_id = InputValidator.get_validated_input("Enter Medicine ID to disable", MedicineValidator.validate_medicine_id)
            if search_id is None: return
            medicine = MedicineManagementLib.dao_service.find_by_medicine_id(search_id)
            if not medicine:
                print("Medicine not found"); return
            print(medicine)
            if not InputValidator.confirm_action("Are you sure you want to disable this medicine?"):
                print("Disable cancelled."); return
            if MedicineManagementLib.dao_service.disable_medicine(search_id):
                print("Medicine disabled successfully.")
            else:
                print("Failed to disable medicine.")
        except Exception as e:
            print(f"Error disabling medicine: {e}")

    @staticmethod
    def search_by_medicine_id():
        try:
            print("\n" + "="*60)
            print("SEARCH MEDICINE".center(60))
            print("="*60)
            search_id = InputValidator.get_validated_input("Enter Medicine ID to search", MedicineValidator.validate_medicine_id)
            if search_id is None: return
            medicine = MedicineManagementLib.dao_service.find_by_medicine_id(search_id)
            if not medicine:
                print("Medicine not found"); return
            print("Medicine Details:")
            print(medicine)
            print("Type:", medicine.get_medicine_type())
            status = "Expired" if medicine.is_expired() else ("Critical Stock" if medicine.is_critical_stock() else "Normal")
            print("Status:", status)
            if medicine.is_expired():
                print("Expired on:", medicine.get_expiry_date())
            if medicine.is_critical_stock():
                print(f"Critical stock: Only {medicine.get_quantity_in_stock()} units remaining")
        except Exception as e:
            print(f"Error searching medicine: {e}")

    @staticmethod
    def search_by_medicine_type():
        try:
            print("\n" + "="*60)
            print("SEARCH BY MEDICINE TYPE".center(60))
            print("="*60)
            available_types = MedicineManagementLib.dao_service.get_medicine_types()
            if not available_types:
                print("No medicine types found in database"); return
            for i, med_type in enumerate(available_types, 1):
                print(f"{i}. {med_type}")
            while True:
                choice = input(f"Select type (1-{len(available_types)}): ").strip()
                try:
                    c = int(choice)
                    if 1 <= c <= len(available_types):
                        selected_type = available_types[c - 1]
                        break
                    else:
                        print("Enter a number shown above.")
                except ValueError:
                    print("Enter a valid number.")
            medicines = MedicineManagementLib.dao_service.find_by_medicine_type(selected_type)
            if not medicines:
                print(f"No medicines found for type: {selected_type}"); return
            print(f"{selected_type.upper()} medicines ({len(medicines)} found):")
            for i, medicine in enumerate(medicines, 1):
                print(f"{i}. {medicine}")
                if medicine.is_expired():
                    print("   [!] This medicine has expired.")
                elif medicine.is_critical_stock():
                    print(f"   [!] Critical stock: {medicine.get_quantity_in_stock()} units.")
        except Exception as e:
            print(f"Error searching by type: {e}")

    @staticmethod
    def show_stock_alerts():
        try:
            print("\n" + "="*60)
            print("STOCK ALERTS".center(60))
            print("="*60)
            crit = MedicineManagementLib.dao_service.get_critical_stock_medicines()
            if not crit:
                print("No medicines at or below critical stock level (10 units or less).")
            else:
                print(f"Critical stock medicines (<=10 units):")
                for med in crit:
                    print(f" {med.get_medicine_name()} (ID: {med.get_medicine_id()}), Stock: {med.get_quantity_in_stock()}")
        except Exception as e:
            print(f"Error checking stock alerts: {e}")

    @staticmethod
    def show_medicine_statistics():
        try:
            print("\n" + "="*80)
            print("MEDICINE STATISTICS".center(80))
            print("="*80)
            medicines = MedicineManagementLib.dao_service.display_all_medicine()
            if not medicines:
                print("No medicines found in inventory.")
                return
            stats = {}
            for med in medicines:
                mt = med.get_medicine_type()
                stats.setdefault(mt, {"count": 0, "stock": 0, "expired": 0, "critical": 0})
                stats[mt]["count"] += 1
                stats[mt]["stock"] += med.get_quantity_in_stock()
                if med.is_expired():
                    stats[mt]["expired"] += 1
                if med.is_critical_stock():
                    stats[mt]["critical"] += 1
            print(f"{'Type':<15} {'Count':<8} {'Stock':<8} {'Expired':<8} {'Critical':<8}")
            for t, s in stats.items():
                print(f"{t:<15} {s['count']:<8} {s['stock']:<8} {s['expired']:<8} {s['critical']:<8}")
        except Exception as e:
            print(f"Error generating statistics: {e}")
