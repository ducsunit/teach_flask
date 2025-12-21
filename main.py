# Flask: Class chính tạo ra ứng dụng
# jsonify: Hàm hỗ trợ chuyển đổi từ Python(Dict, List) thành json
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

courses = [
    # key : value
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

"""
@app.route -> Decorator(@)
-> Nhiệm vụ của nó là đăng kí Flask là nếu có thg nào gọi vào /courses
thì chạy cái hàm get_all_courses()
"""
@app.route('/courses', methods=['GET'])
def get_all_courses():
    return jsonify(courses)

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    for c in courses:
        if c['id'] == course_id:
            return jsonify(c)
        
    return jsonify({
        'error': 'Không tìm thấy khóa học'
    })

@app.route("/courses", methods=['POST'])
def create_course():
    # request.get_json() -> Mở cái gói tin mà người dùng POST lên 
    # đọc cái phần Body, ép kiểu từ thag json sang dict or list
    # nếu mà người dùng gửi linh tinh có thể trả về None
    """
        => new_data
        {
            "name": "Learn abc"
            "price": 1231
        }
    """
    new_data = request.get_json()

    if not new_data or 'name' not in new_data:
        """
       400 bad request
       status code: 200 -> OK, 201 -> created ok, 500 -> Internal server, 403 -> xác thực, 404 -> not found
       401 -> phân quyền, 405 -> không đúng method
        """
        return jsonify(
            {
                'error': 'Thiếu tên khóa học'
            }
        ), 400
    
    """
    0 1 2 3 4
    a b c d e
    """
    if len(courses) > 0:
        new_id = courses[-1]['id'] + 1 
    else: # list rỗng
        new_id = 1
    
    # tạo dict cho khóa học mới
    new_course = {
        "id": new_id,
        "name": new_data['name'],
        "description": new_data['description'],
        "price": new_data['price']
    }

    # thêm vào cuối list -> database fake
    courses.append(new_course)

    return jsonify(new_course), 201

# <int:course_id> -> Path parameter
# Flask tự động ép tham số sang số nguyên -> URL courses/1 gán vào course_id
@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course_can_tim = None 

    for c in courses:
        if c['id'] == course_id:
            course_can_tim = c
            break

    # xử lý lỗi nếu không tìm thấy
    if not course_can_tim:
        return jsonify(
            {
                'error': 'Không tìm thầy khóa học'
            }
        ), 404
    
    # Lấy dữ liệu người dùng gửi lên
    json_data = request.get_json()

    # Cập nhật dữ liệu
    """
    json_data.get('name', course_can_tim['name'])
    - Hãy lấy giá trị name mà người dùng gửi lên 
    - Nếu người dùng k gửi giá trị này lên thì giữ nguyên giá trị cũ trong course_can_tim
    """
    course_can_tim['name'] = json_data.get('name', course_can_tim['name'])
    course_can_tim['description'] = json_data.get('desciption', course_can_tim['description'])
    course_can_tim['price'] = json_data.get('price', course_can_tim['price'])

    # trả về kết quả
    return jsonify(course_can_tim)

# 
@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course_can_xoa = None

    for c in courses:
        if c['id'] == course_id:
            course_can_xoa = c
            break
    
    if not course_can_xoa:
        return jsonify(
            {
                'error': 'Không tìm thầy khóa học'
            }
        ), 404

    courses.remove(course_can_xoa)

    # status code 204 -> No content
    return jsonify(
        {
            'result': True,
            'message': 'Xóa thành công'
        }
    )


# Kiểm tra xem file này có chạy trực tiếp hay không

if __name__ == "__main__":
    # Lệnh chạy server có sẵn trong Flask
    # Bật debug 
    app.run(debug=True)