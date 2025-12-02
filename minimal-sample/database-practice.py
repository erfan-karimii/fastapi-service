from typing import List
from sqlalchemy import create_engine ,SmallInteger, String , TEXT , ForeignKey , CheckConstraint , select   , delete
from sqlalchemy.orm import sessionmaker , relationship , Mapped , mapped_column , DeclarativeBase
from datetime import datetime


engine = create_engine('sqlite:///example.db',echo=True)
LocalSession = sessionmaker(bind=engine,autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = 'student'
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(256))
    age : Mapped[int] = mapped_column()
    courses :Mapped[List["Course"]]  = relationship(secondary="enrollment", back_populates="students")

    def __repr__(self):
        return f"Student(id={self.id},name={self.name},age={self.age})"


class Course(Base):
    __tablename__ = 'course'
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column(TEXT)
    assignments :Mapped[List["Assignment"]]  = relationship(backref="course")
    students :Mapped[List["Student"]]  = relationship(secondary="enrollment", back_populates="courses")

    def __repr__(self):
        return f"Course(id={self.id},title={self.title},description={(self.description or '')[:20]})"


class Enrollment(Base):
    __tablename__ = 'enrollment'
    id : Mapped[int] = mapped_column(primary_key=True)
    course_id : Mapped[int] = mapped_column(ForeignKey("course.id"))
    student_id : Mapped[int] = mapped_column(ForeignKey("student.id"))

    grade : Mapped[int] = mapped_column(SmallInteger,default=0)
    created_at : Mapped[datetime] = mapped_column(default=datetime.now)

    __table_args__ = (
        CheckConstraint('grade <= 100', name='check_grade_max_100'),
        CheckConstraint('grade >= 0', name='check_grade_min_0'),
    )

    def __repr__(self):
        return f"Enrollment(id={self.id},course_id={self.course_id},student_id={self.student_id})"


class Assignment(Base):
    __tablename__ = 'sssignment'
    id : Mapped[int] = mapped_column(primary_key=True)
    course_id : Mapped[int] = mapped_column(ForeignKey("course.id"))
    title : Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column(TEXT,nullable=True)
    # TODO: add upload file to this table 
    def __repr__(self):
        return f"Assignment(id={self.id},course_id={self.course_id},title={self.title})"


Base.metadata.create_all(engine)
session = LocalSession()



# stmt = select(Course).where(Course.title == "django")
# course_django = session.execute(stmt).scalars().first()
# print(course_django)

stmt = select(Student).where(Student.name == "erfan")
student_erfan = session.execute(stmt).scalars().first()
print(student_erfan,student_erfan.courses) 


# stmt = select(Assignment).where(Assignment.id == 1)
# django_assignment = session.execute(stmt).scalars().first()
# print(django_assignment)

# stmt = select(Enrollment).where(Enrollment.id == 1)
# enroll_erfan_django = session.execute(stmt).scalars().first()
# print(enroll_erfan_django)

