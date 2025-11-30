from data.db_session import create_session, global_init
from data.users import User
from data.texts import Text

global_init("db/db.db")


db_session = create_session()


data = []
for user in db_session.query(User).all():
    print(vars(user))
    data.append(user)
print(data)

data = []
for user in db_session.query(Text).all():
    print(vars(user))
    data.append(user)
print(data)
