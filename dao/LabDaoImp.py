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

    DISPLAY_ALL = "SELECT * FROM lab_tests"

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
            print("Error fetching tests:", e)
        finally:
            cursor.close()
        return products
