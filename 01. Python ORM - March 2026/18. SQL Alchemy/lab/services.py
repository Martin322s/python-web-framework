from main import Session
from models import User

with Session() as session:
    user = session.query(User).filter_by(username="admin").first()

    if user:
        session.delete(user)
        session.commit()
        print('User updated successfully')
    else:
        print('User not found')