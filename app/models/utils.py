from app.database import db_session


class ModelMixin(object):
    def save(self, do_commit=True):
        # Save this model to the database.
        db_session.add(self)
        if do_commit:
            try:
                db_session.commit()
            except:
                db_session.rollback()
                raise
        return self

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        return self
