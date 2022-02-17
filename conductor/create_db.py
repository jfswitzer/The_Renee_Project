import db
with db.db:
    db.db.create_tables([db.Device, db.Job])