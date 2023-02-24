from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, email):
        director = self.get_by_email(email)
        self.session.delete(director)
        self.session.commit()

    def update(self, user_d, email):
        user = self.get_by_email(email)
        if user_d.get('name'):
            user.name = user_d.get('name')
        if user_d.get('surname'):
            user.surname = user_d.get('surname')
        if user_d.get('favorite_genre'):
            user.favorite_genre = user_d.get('favorite_genre')

        self.session.add(user)
        self.session.commit()

    def update_password(self, user_d, email):
        user = self.get_by_email(email)
        user.password = user_d.get('password')

        self.session.add(user)
        self.session.commit()
