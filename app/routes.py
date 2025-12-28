# Blueprint -> chia code thành các module
# web module auth -> xác thực, course -> khóa học, cart -> giỏ hàng 
from calendar import c
from hmac import new
from shutil import ExecError
from flask import Blueprint, jsonify, request, abort

from .models import Course

from .extensions import db
# course -> tên để đăng kí url
# abort()
course_bp = Blueprint('course', __name__)

# RESTful API
# courses = [
#     {
#         "id": 1,
#         "name": "Lập trình Java",
#         "description": "Full snack 2025",
#         "price": 150000 
#     },
#     {
#         "id": 2,
#         "name": "Lập trình Python",
#         "description": "Full snack 2025",
#         "price": 99000 
#     },
#     {
#         "id": 3,
#         "name": "Lập trình C",
#         "description": "Full snack 2025",
#         "price": 50000 
#     },

# ]

# API lấy danh sách khóa học -> GET
@course_bp.route("/courses", methods=['GET'])
def get_all_courses():

    # Course.query.all()
    '''
    - Nhiệm vụ -> "SELECT * FROM courses" -> MySQL
    - Kết quả trả về : List các object (VD: [<Object1>, <Object2>])
    - Lưu ý: Nó KHÔNG trả về JSON hay Dictionary.
    '''
    course_objects = Course.query.all()
    course_json = []

    for course in course_objects:
        course_json.append({
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "price": course.price
        })
    return jsonify(course_json)

# lấy khóa học theo id
@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = db.session.get(Course, course_id)

    if not course:
        return abort(404)
    
    return jsonify({
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "price": course.price
    })

@course_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()

    if not data or 'name' not in data:
        abort(400, description="Thiếu tên khóa học")

    new_course = Course(name=data['name'], 
                        description=data['description'],
                        price=data['price'])
    
    try:
        # sẽ lưu nhưng chưa lưu xuống db ngay
        db.session.add(new_course)

        db.session.commit()
    except Exception as e:
        db.session.rollback()

        return jsonify({'error': str(e)}), 500

    return jsonify({
        "id": new_course.id,
        "name": new_course.name,
        "description": new_course.description,
        "price": new_course.price
    }), 201

@course_bp.route('/courses/<int:course_id>', methods=['PUT']) 
def update_course(course_id):
    '''
    Docstring for update_course
    
    :param course_id: id course

    - Nhiệm vụ: Tìm trong bảng courses dòng có id == course_id
    - <=> SELECT * FROM course WHERE id = 5
    '''
    course = db.session.get(Course, course_id)

    if not course:
        return abort(404)
    
    data = request.get_json()

    '''
    - get lấy name trong dữ liệu mình gửi lên
    - nếu có dữ liệu bị thay đổi gán lại cho course.name 
    - nếu không giữ nguyên
    '''
    course.name = data.get('name', course.name)
    course.description = data.get('description', course.description)
    course.price = data.get('price', course.price)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return abort(500)
    
    return jsonify({
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "price": course.price
    })

@course_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = db.session.get(Course, course_id)

    if not course:
        return abort(404)
    
    try:
        db.session.delete(course)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return abort(500)
    
    return jsonify({
        "result": True,
        "message": "Đã xóa thành công khỏi Database !"
    })


