from db import get_db

class Animal:
    def __init__(self, id_, name, user_id, kind, breed, sex, age, description, img_url, location, adopted=0):
        self.id = id_
        self.name = name
        self.user_id = user_id
        self.kind = kind
        self.breed = breed
        self.sex = sex
        self.age = age
        self.description = description
        self.img_url = img_url
        self.location = location
        self.adopted = adopted

    @staticmethod
    def remove(animal_id):
        db = get_db()
        db.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
        db.commit()


    @staticmethod
    def get(animal_id):
        db = get_db()
        animal = db.execute(
            "SELECT * FROM animals WHERE id = ?", (animal_id,)
        ).fetchone()
        if not animal:
            return None

        animal = Animal(
            id_=animal[0], name=animal[1], user_id=animal[2], kind=animal[3], breed=animal[4],
            sex=animal[5], age=animal[6], description=animal[7], img_url=animal[8], location=animal[9]
        )
        return animal

    @staticmethod
    def create(name, user_id, kind, breed, sex, age, description, img_url, location):
        db = get_db()
        db.execute(
            "INSERT INTO animals (name, user_id, kind, breed, sex, age, description, img_url, location)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, user_id, kind, breed, sex, age, description, img_url, location),
        )
        db.commit()

    @staticmethod
    def setAdopted(animal_id):
        db = get_db()
        db.execute("UPDATE animals SET adopted = 'true' WHERE id=?", (animal_id,))
        db.commit()
    @staticmethod
    def get_all(page, per_page):
        db = get_db()

        # Calculate the offset based on the page number and items per page
        offset = (page - 1) * per_page

        # Fetch animals for the requested page
        animals = db.execute(
            "SELECT * FROM animals WHERE adopted='0' LIMIT ? OFFSET ?",
            (per_page, offset)
        ).fetchall()

        animal_list = []
        for animal in animals:
            animal_obj = Animal(
                id_=animal[0], name=animal[1], user_id=animal[2], kind=animal[3], breed=animal[4],
                sex=animal[5], age=animal[6], description=animal[7], img_url=animal[8], location=animal[9]
            )
            animal_list.append(animal_obj)

        return animal_list
