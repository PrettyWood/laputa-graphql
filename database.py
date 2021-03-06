from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///laputa.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import SmallApp, Group, User, PrivilegeEnum, Privilege, Role, Comment
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Small Apps
    demo = SmallApp(id='demo', name='demoo')
    db_session.add(demo)
    nani = SmallApp(id='nani', name='nanoo')
    db_session.add(nani)

    # Groups
    manager = Group(name='manager')
    db_session.add(manager)
    dev = Group(name='developer')
    db_session.add(dev)

    # Users
    eric = User(name='eric@test.com', groups=[manager, dev], role=Role.SUPER_ADMIN)
    db_session.add(eric)
    laure = User(name='laure.jolibois@test.manager.com', groups=[manager], created_by=eric,
                 password_email_sent=True)
    db_session.add(laure)
    fred = User(name='fred@TEST.com', groups=[dev], created_by=eric, role=Role.ADMIN)
    db_session.add(fred)

    # Privileges
    privilege1 = Privilege(user=eric, small_app=demo, privilege=PrivilegeEnum.CONTRIBUTE)
    db_session.add(privilege1)
    privilege2 = Privilege(user=eric, small_app=nani, privilege=PrivilegeEnum.CONTRIBUTE)
    db_session.add(privilege2)
    privilege3 = Privilege(user=fred, small_app=demo, privilege=PrivilegeEnum.CONTRIBUTE)
    db_session.add(privilege3)
    privilege4 = Privilege(user=fred, small_app=nani, privilege=PrivilegeEnum.VIEW)
    db_session.add(privilege4)
    privilege5 = Privilege(user=laure, small_app=demo, privilege=PrivilegeEnum.VIEW)
    db_session.add(privilege5)

    # Comments
    comment1 = Comment(user=eric, small_app=demo, slide_id=420, message='Toucan Toco rocks!')
    db_session.add(comment1)
    comment2 = Comment(user=fred, small_app=demo, slide_id=420, message='Toucan Toco rocks indeed!')
    db_session.add(comment2)
    comment3 = Comment(user=eric, small_app=demo, slide_id=666,
                       message='Did I say that Toucan Toco rocks?')
    db_session.add(comment3)

    db_session.commit()
