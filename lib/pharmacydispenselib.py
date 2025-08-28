from dao.pharmadispensedao import PharmacyDispenseDao

class PharmacyDispenseService:
    dao = PharmacyDispenseDao()

    @staticmethod
    def view_pending_prescriptions():
        prescriptions = PharmacyDispenseService.dao.get_pending_prescriptions()
        
        if not prescriptions:
            print("\nNo pending prescriptions to dispense.")
            return
        
        print("\n" + "="*80)
        print("PENDING PRESCRIPTIONS FOR DISPENSING")
        print("="*80)
        print(f"{'ID':<6} {'Prescription':<12} {'Patient':<15} {'Medicine':<20} {'Qty':<8} {'Stock':<8} {'Dosage'}")
        print("-"*80)
        
        for rx in prescriptions:
            print(f"{rx['med_prescription_id']:<6} {rx['prescription_id']:<12} {rx['patient_name']:<15} "
                  f"{rx['medicine_name']:<20} {rx['medicine_quantity']:<8} {rx['quantity_in_stock']:<8} {rx['dosage']}")
        print("="*80)

    @staticmethod
    def dispense_and_bill():
        try:
            PharmacyDispenseService.view_pending_prescriptions()
            
            med_prescription_id = int(input("\nEnter med_prescription_id to dispense: "))
            quantity = int(input("Enter quantity to dispense: "))
            
            # Get prescription details
            prescriptions = PharmacyDispenseService.dao.get_pending_prescriptions()
            prescription = next((p for p in prescriptions if p['med_prescription_id'] == med_prescription_id), None)
            
            if not prescription:
                print("Invalid med_prescription_id.")
                return
                
            if quantity > prescription['medicine_quantity']:
                print(f"Cannot dispense more than prescribed quantity: {prescription['medicine_quantity']}")
                return
            
            success, message = PharmacyDispenseService.dao.dispense_medicine(
                med_prescription_id, 
                prescription['medicine_id'], 
                quantity, 
                prescription['appointment_id']
            )
            
            if success:
                print("SUCCESS:", message)
                print("Bill generated automatically.")
            else:
                print("ERROR:", message)
                
        except ValueError:
            print("Please enter valid numbers.")
        except Exception as e:
            print("Error during dispensing:", e)

    @staticmethod
    def print_bill():
        try:
            appointment_id = int(input("Enter appointment_id for bill: "))
            
            items, total = PharmacyDispenseService.dao.get_bill_for_appointment(appointment_id)
            
            if not items:
                print("No billing information found for this appointment.")
                return
            
            print("\n" + "="*60)
            print("PHARMACY BILL")
            print("="*60)
            print(f"Appointment ID: {appointment_id}")
            if items:
                print(f"Patient: {items[0]['patient_name']}")
            print("-"*60)
            print(f"{'Medicine':<25} {'Qty':<8} {'Price':<10} {'Total':<12}")
            print("-"*60)
            
            for item in items:
                print(f"{item['medicine_name']:<25} {item['quantity_dispensed']:<8} "
                      f"{item['unit_price']:<10} {item['total_amount']:<12.2f}")
            
            print("-"*60)
            print(f"{'TOTAL AMOUNT':<45} {total:>12.2f}")
            print("="*60)
            
        except ValueError:
            print("Please enter a valid appointment ID.")
        except Exception as e:
            print("Error generating bill:", e)
