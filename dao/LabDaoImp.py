from dao.abstractLabDao import AbstractLabDao
from models.labtech import LabTech
from db.db_connection import DBConnection
from pymysql.cursors import DictCursor
from typing import List

class LabDaoimplementation(AbstractLabDao):

    INSERT_LABTECH = """
    INSERT INTO lab_tests(test_id, test_name, test_category, normal_range_min, normal_range_max, unit_of_measurement, test_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    DISPLAY_ALL = "SELECT * FROM lab_tests where is_active = 1"
    FIND_BY_ID =  "SELECT  * FROM lab_tests WHERE test_id = %s"
    UPDATE_TEST = """
        UPDATE lab_tests 
        SET test_name = %s, 
            unit_of_measurement = %s, 
            test_price = %s
        WHERE test_id = %s AND is_active = 1
    """
    DISABLE = "UPDATE lab_tests SET is_active = 0 WHERE test_id = %s AND is_active = 1 LIMIT 1"
    
    ADD_TEST_RESULT = """
        INSERT INTO lab_results (test_prescription_id, test_value, result_status, tested_date)
        VALUES (%s, %s, %s, %s)
    """

    VIEW_PRESCRIPTION_RESULTS = """
        SELECT tp.test_prescription_id,
               tp.prescription_id,
               tp.test_name,
               lr.result_id,
               lr.test_value,
               lr.result_status,
               lr.tested_date
        FROM test_prescription tp
        LEFT JOIN lab_results lr
               ON tp.test_prescription_id = lr.test_prescription_id
    """

    LIST_ALL_RESULTS = """
        SELECT lr.result_id,
               lr.test_prescription_id,
               tp.prescription_id,
               tp.test_name,
               lr.test_value,
               lr.result_status,
               lr.tested_date
        FROM lab_results lr
        JOIN test_prescription tp ON lr.test_prescription_id = tp.test_prescription_id
        ORDER BY lr.tested_date DESC, lr.result_id DESC
    """

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def create_test(self, labtech: LabTech) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                self.INSERT_LABTECH,
                (
                    labtech.test_id,
                    labtech.test_name,
                    labtech.test_category,
                    labtech.normal_range_min,
                    labtech.normal_range_max,
                    labtech.unit_of_measurement,
                    labtech.test_price,
                )
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting test:", e)
            return False
        finally:
            cursor.close()

    def display_test(self) -> List[LabTech]:
        products = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                products.append(
                    LabTech(
                        test_id=row["test_id"],
                        test_name=row["test_name"],
                        test_category=row["test_category"],
                        normal_range_min=row["normal_range_min"],
                        normal_range_max=row["normal_range_max"],
                        unit_of_measurement=row["unit_of_measurement"],
                        test_price=row["test_price"],
                    )
                )
        except Exception as e:
            print("Error fetching products:", e)
        finally:
            cursor.close()
        return products
    
    def find_by_test_id(self,test_id:int):
        product = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_ID,(test_id,))
            row = cursor.fetchone()
            if row:
                product = LabTech(
                    test_id=row["test_id"],
                    test_name=row["test_name"],
                    test_category=row["test_category"],
                    normal_range_min=row["normal_range_min"],
                    normal_range_max=row["normal_range_max"],
                    unit_of_measurement=row["unit_of_measurement"],
                    test_price=row["test_price"],
                )
        except Exception as e:
            print("Error finding product:",e)
        finally:
            cursor.close()

        return product
    
   
    def update_test(self, labtech: LabTech, test_id: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.UPDATE_TEST, (
                labtech.test_name,
                labtech.unit_of_measurement,
                labtech.test_price,
                test_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating product:", e)
            return False
        finally:
            cursor.close()

    def delete_test(self, test_id: str) -> bool:
        try:
            cursor = self.conn.cursor()
            # Ensure connection is alive to avoid hanging on network glitches
            try:
                self.conn.ping(reconnect=True)
            except Exception:
                pass
            cursor.execute(self.DISABLE, (test_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error disabling product:", e)
            return False
        finally:
            cursor.close()

    def view_prescription_results(self):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.VIEW_PRESCRIPTION_RESULTS)
            rows = cursor.fetchall()
            return rows or []
        except Exception as e:
            print("Error fetching prescription results:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def add_test_result(self, test_prescription_id: int, test_value: str, 
                        result_status: str, tested_date: str, lab_resultcol: str | None = None) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.ADD_TEST_RESULT, (
                test_prescription_id, test_value, result_status, tested_date
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting test result:", e)
            return False
        finally:
            cursor.close()

    def list_all_test_results(self):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.LIST_ALL_RESULTS)
            return cursor.fetchall() or []
        except Exception as e:
            print("Error listing test results:", e)
            return []
        finally:
            if cursor:
                cursor.close()