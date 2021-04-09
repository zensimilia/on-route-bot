from app.db import db_engine, db_session
from app.models.base import Model
from app.models.user import User
from app.models.route import Route

Model.metadata.create_all(db_engine)


# user = User()
# user.user_id = 9981
# user.username = 'Private Person'

# route = Route()
# route.url = 'https://ya.ru/'
# route.name = 'First route'
# route.user = user

with db_session() as db:
    user = db.query(User).get(1)
    # route.user = user
    # route = db.query(Route).get(1)
    # db.delete(route)
    db.delete(user)
    # db.add(user)
    # db.add(route)

# with db_session() as db:
# user = db.query(User).get(3)
# user.update({'username': 'Hello kitty'})
# print(user)
# db.update(user)

# session.query(User).filter(User.id == 2).delete()
# session.commit()

# user = session.query(User).all()
# print(user)

# user = (
#     session.query(User).filter(User.id == 2).update({
#         'username': 'Updated #2'
#     })
# )
# session.commit()

# user = User(user_id='4321', username='Second User')
# session.add(user)
# session.commit()

# read this https://gist.github.com/nitred/4323d86bb22b7ec788a8dcfcac03b27a

# user = session.query(User).first()
# user.username = 'New Username'
# session.commit()
