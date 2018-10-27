from app import create_app
from app.utils.error import APIException, ServerError
from werkzeug.exceptions import HTTPException

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 当前的未知异常log一下
        if not app.config['DEBUG']:         # 上线运营模式
            return ServerError
        else:                               # 调试模式
            raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888')