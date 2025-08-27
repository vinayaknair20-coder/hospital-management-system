class Consultation:
    def __init__(self,appointment_id,symptoms,diagnosis,consultation_notes,doctor_id):
        self.__appointment_id=appointment_id
        self.__symptoms=symptoms
        self.__diagnosis=diagnosis
        self.__consultation_notes=consultation_notes
        self.__doctor_id=doctor_id
       
        

    # getters
    @property
    def appointment_id(self):
        return self.__appointment_id

    @property
    def symptoms(self):
        return self.__symptoms
    
    @property
    def diagonis(self):
        return self.__diagnosis
    
    @property
    def consultation_notes(self):
        return self.__consultation_notes
    
    @property
    def doctor_id(self):
        return self.__doctor_id
    
    # @property
    # def consultation_date(self):
    #     return self.__consultation_date

    def __str__(self):
        return f'appointment_id ={self.__appointment_id},symptoms={self.__symptoms},diagnosis={self.__diagnosis},consultation_notes={self.__consultation_notes},doctor_id={self.__doctor_id}'