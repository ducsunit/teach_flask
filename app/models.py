from .extensions import db

class Course(db.Model):
    
    __tablename__ = "courses"

    # định nghĩa các cột
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    description = db.Column(db.String(200), nullable=False)

    price = db.Column(db.Float, default=0)

    # in đối tượng để debug
    def __repr__(self):
        return f"Courses: id={self.id}, name={self.name}, description={self.description}, price={self.price} "