from flask import jsonify

def register_error_handlers(app):

    # 404 -> Not Found
    @app.errorhandler(404)
    def handle_404_error(error):
        return jsonify({
            'error_code': 404,
            'message': 'Không tìm thấy yêu cầu (Not Found)',
            'detail': 'Vui lòng kiểm tra lại URL hoặc ID'
        }), 404
    
    # 500 -> Internal Servel Error
    @app.errorhandler(500)
    def handle_500_error(error):
        return jsonify({
            'error_code': 500,
            'message': 'Lỗi hệ thống', 
            'detail': 'Đã có sự cố xảy ra phía server. Vui lòng thử lại'
        }), 500
    
    # 400 -> Bad request
    @app.errorhandler(400)
    def handle_400_error(error):
        return jsonify({
            'error_code': 400,
            'message': 'Yêu cầu không hợp lệ',
            'detail': str(error.description)
        }), 400