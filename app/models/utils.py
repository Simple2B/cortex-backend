from app.database import db_session


class ModelMixin(object):
    def save(self, do_commit=True):
        # Save this model to the database.
        db_session.add(self)
        if do_commit:
            db_session.commit()
        return self

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        return self
