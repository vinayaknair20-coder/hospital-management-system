class LabTech:
    def __init__(
        self,
        test_id=None,
        test_name=None,
        test_category=None,         
        normal_range_min=None,
        normal_range_max=None,
        unit_of_measurement=None,
        test_price=None,
    ):
        self.__testid = test_id
        self.__testname = test_name
        self.__testcategory = test_category
        self.__rangemin = normal_range_min
        self.__rangemax = normal_range_max
        self.__measurement = unit_of_measurement
        self.__testprice = test_price

    # --- Properties (Pythonic way) ---

    @property
    def test_id(self):
        return self.__testid

    @test_id.setter
    def test_id(self, value):
        self.__testid = value

    @property
    def test_name(self):
        return self.__testname

    @test_name.setter
    def test_name(self, value):
        self.__testname = value

    @property
    def test_category(self):
        return self.__testcategory

    @test_category.setter
    def test_category(self, value):
        self.__testcategory = value

    @property
    def normal_range_min(self):
        return self.__rangemin

    @normal_range_min.setter
    def normal_range_min(self, value):
        self.__rangemin = value

    @property
    def normal_range_max(self):
        return self.__rangemax

    @normal_range_max.setter
    def normal_range_max(self, value):
        self.__rangemax = value

    @property
    def unit_of_measurement(self):
        return self.__measurement

    @unit_of_measurement.setter
    def unit_of_measurement(self, value):
        self.__measurement = value

    @property
    def test_price(self):
        return self.__testprice

    @test_price.setter
    def test_price(self, value):
        self.__testprice = value

    # --- String Representations ---

    def __str__(self):
        return (
            f"id={self.test_id}, "
            f"name={self.test_name}, "
            f"category={self.test_category}, "
            f"Minimum_range={self.normal_range_min}, "
            f"Maximum_range={self.normal_range_max}, "
            f"Measurement={self.unit_of_measurement}, "
            f"Price={self.test_price}"
        )

    def __repr__(self):
        return self.__str__()
