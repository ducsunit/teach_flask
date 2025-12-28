# Blueprint -> chia code thành các module
# web module auth -> xác thực, course -> khóa học, cart -> giỏ hàng 
from flask import Blueprint, jsonify, request, abort

from .models import Course
# course -> tên để đăng kí url
# abort()
course_bp = Blueprint('course', __name__)

# RESTful API
courses = [
    {
        "id": 1,
        "name": "Lập trình Java",
        "description": "Full snack 2025",
        "price": 150000 
    },
    {
        "id": 2,
        "name": "Lập trình Python",
        "description": "Full snack 2025",
        "price": 99000 
    },
    {
        "id": 3,
        "name": "Lập trình C",
        "description": "Full snack 2025",
        "price": 50000 
    },

]

def find_course(course_id):
    for c in courses:
        if c['id'] == course_id:
            return c
    return None

@course_bp.route('/courses', methods=['GET'])
def get_all_course():
    return jsonify(courses)

@course_bp.route('/courses', methods=['POST'])
def create_course():
    # lấy dữ liệu người dùng gửi lên
    new_data = request.get_json()

    # Kiểm tra dữ liệu gửi lên có đúng không
    if not new_data or 'name' not in new_data:
        abort(400, description='Thiếu tên khóa học')
    
    # tạo id mới
    if len(courses) > 0:
        new_id = courses[-1]['id'] + 1
    else:
        new_id = 1
    
    # tạo khóa học mới 
    new_course = {
        "id": new_id,
        "name": new_data['name'],
        "description": new_data['description'],
        "price": new_data['price']
    }

    # lưu dữ liệu 
    courses.append(new_course)

    # trả kết quả về
    return jsonify(new_course), 201 

@course_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course_can_update = find_course(course_id)
    
    # kiểm tra nếu không tìm được
    if course_can_update is None:
        abort(404)
    
    json_data = request.get_json()
    # Cập nhật thông tin
    course_can_update['name'] = json_data.get('name', course_can_update['name'])
    course_can_update['description'] = json_data.get('description', course_can_update['description'])
    course_can_update['price'] = json_data.get('price', course_can_update['price'])

    return jsonify(course_can_update)

@course_bp.route('/courses/<int:course_id>', methods=["DELETE"])
def delete_course(course_id):
    course_can_xoa = find_course(course_id)

    if course_can_xoa is None:
        abort(404)
    
    courses.remove(course_can_xoa)

    return jsonify({
        'result': True,
        'message': 'Xóa thành công'
    })


