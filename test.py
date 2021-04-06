from app.models.base import Model, engine, session
from app.models.user import User

Model.metadata.create_all(engine)

# user = User()
# user.user_id = '1234'
# user.username = 'Test user'
# session.add(user)
# session.commit()

# user = session.query(User).all()
# print(user)

# user = User(user_id='4321', username='Second User')
# session.add(user)
# session.commit()

# read this https://gist.github.com/nitred/4323d86bb22b7ec788a8dcfcac03b27a

user = session.query(User).first()
user.username = 'New Username'
session.commit()
