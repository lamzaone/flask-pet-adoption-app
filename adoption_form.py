from db import get_db

class AdoptionForm:
    def __init__(self, user_id, animal_id, owner_id, user_age, location, building_type, current_pets, previous_experience, phone_number, status = None):
        self.user_id = user_id
        self.animal_id = animal_id
        self.owner_id = owner_id
        self.user_age = user_age
        self.location = location
        self.building_type = building_type
        self.current_pets = current_pets
        self.previous_experience = previous_experience
        self.phone_number = phone_number
        self.status = status

    @staticmethod
    def create(user_id, animal_id, owner_id, user_age, location, building_type, current_pets, previous_experience, phone_number):
        db = get_db()
        db.execute(
            "INSERT INTO adoption_forms (user_id, animal_id, owner_id, user_age, location, building_type, current_pets, previous_experience, phone_number)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, animal_id, owner_id, user_age, location, building_type, current_pets, previous_experience, phone_number),
        )
        db.commit()

    @staticmethod
    def remove(user_id, animal_id):
        db = get_db()
        db.execute("DELETE FROM adoption_forms WHERE user_id = ? AND animal_id=?", (user_id, animal_id))
        db.commit()

    def setStatus(user_id, animal_id, status):
        db = get_db()
        db.execute("UPDATE adoption_forms SET status = ? WHERE user_id = ? AND animal_id=?", (status, user_id, animal_id))
        db.commit()


    @staticmethod
    def get_all():
        db = get_db()
        adoption_forms = db.execute("SELECT * FROM adoption_forms").fetchall()

        forms_list = []
        for form in adoption_forms:
            form_obj = AdoptionForm(
                user_id=form[0], animal_id=form[1], owner_id=form[2], user_age=form[3],
                location=form[4], building_type=form[5], current_pets=form[6],
                previous_experience=form[7], phone_number=form[8], status=form[9]
            )
            forms_list.append(form_obj)

        return forms_list

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        adoption_forms = db.execute(
            "SELECT * FROM adoption_forms WHERE user_id = ?",
            (user_id,)
        ).fetchall()

        forms_list = []
        for form in adoption_forms:
            form_obj = AdoptionForm(
                user_id=form[0], animal_id=form[1], owner_id=form[2], user_age=form[3],
                location=form[4], building_type=form[5], current_pets=form[6],
                previous_experience=form[7], phone_number=form[8], status=form[9]
            )
            forms_list.append(form_obj)

        return forms_list
    @staticmethod
    def get_all_by_owner(owner_id):
        db = get_db()
        adoption_forms = db.execute(
            "SELECT * FROM adoption_forms WHERE owner_id = ? AND status = ?",
            (owner_id,"pending",)
        ).fetchall()

        forms_list = []
        for form in adoption_forms:
            form_obj = AdoptionForm(
                user_id=form[0], animal_id=form[1], owner_id=form[2], user_age=form[3],
                location=form[4], building_type=form[5], current_pets=form[6],
                previous_experience=form[7], phone_number=form[8], status=form[9]
            )
            forms_list.append(form_obj)

        return forms_list