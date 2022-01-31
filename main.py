from flask import Flask, request

import marshmallow, jsonify, pms_command
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return {'error': 'Unauthorized access'}


# lv_rc = pms_command.chk_connect()
# print("RET: " + pms_command.get_sys_var('DB8', '\<DEF_HOST\>'))
# print("Change to proc rc:" + str(pms_command.set_sys_var('DB8', '\<DEF_HOST\>', 'p1-lnw_OK')))
# print("RET: " + pms_command.get_sys_var('DB8', '\<DEF_HOST\>'))
# pms_db.get_syslist()

app = Flask(__name__)


@app.route("/api/get_var", methods=['POST', 'GET'])
@auth.login_required
def get_var():
    lv_grc = ""
    if request.method == 'POST':
        ls_sys_name = request.args.get('sys_name')
        ls_var_name = request.args.get('var_name')
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'ACT: get variable value to {ls_sys_name}-{ls_var_name}')
            print("--> RET: " + pms_command.get_sys_var(f'{ls_sys_name}', f'\<{ls_var_name}\>'))
            lv_grc = 0
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMS server connection ERROR"

    return str(lv_grc)


@app.route("/api/start_cmd", methods=['POST'])
@auth.login_required
def api_start_cmd():
    print("kokokokk")
    return "Adom maar...."


@app.route("/api/set_var", methods=['POST'])
@auth.login_required
def api_set_var():
    lv_grc = -1
    if request.method == 'POST':
        ls_sys_name = request.args.get('sys_name')
        ls_var_name = request.args.get('var_name')
        ls_var_value = request.args.get('var_value')
        lv_rc = pms_command.chk_connect()
        if lv_rc == 0:
            print(f'Act: set variable value to {ls_sys_name}-{ls_var_name} value: {ls_var_value}')
            print("--> RC : " + str(pms_command.set_sys_var(f'{ls_sys_name}', f'\<{ls_var_name}\>', f'{ls_var_value}')))
            print("--> RET: " + pms_command.get_sys_var(f'{ls_sys_name}', f'\<{ls_var_name}\>'))
            lv_grc = 0
        else:
            print("PMS server connection ERROR")
            lv_grc = "PMS server connection ERROR"

    return str(lv_grc)


if __name__ == "__main__":
    app.run(debug=True)
