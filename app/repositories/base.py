from app.extensions import db

class BaseRepository:
    model = None
    def list(self, **filters):
        query = self.model.query.filter_by(**{k:v for k,v in filters.items() if v is not None})
        return query
    def get(self, id): return self.model.query.get_or_404(id)
    def create(self, data):
        obj = self.model(**data); db.session.add(obj); db.session.commit(); return obj
    def update(self, obj, data):
        for key, value in data.items(): setattr(obj, key, value)
        db.session.commit(); return obj
    def delete(self, obj): db.session.delete(obj); db.session.commit()
