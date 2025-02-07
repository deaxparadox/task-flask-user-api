def get_fields(model):
    return [c.name for c in model.__table__.columns]