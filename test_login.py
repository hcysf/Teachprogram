import json

import  pytest
from src.login_request import ReDate
from  data.test_login import login_test_data

class Testlogin:
    correct_code=2

    #夹具 clint 客户端
    @pytest.fixture(scope="function")
    def clinet(self):
        client=ReDate()
        yield client
        client.close_session()

    # 夹具获取验证码
    @pytest.fixture(scope="function")
    def get_uuid(self,clinet):
        response=clinet.get_captchaImage()
        assert response.status_code == 200
        data = response.json()
        return {"uuid": data["uuid"]}

    #夹具获取登录测试用例
    @pytest.mark.parametrize("test_data",login_test_data)
    def test_login(self,clinet,get_uuid,test_data):
        id=test_data['id']
        descripiton=test_data['descripiton']
        username=test_data['username']
        password=test_data['password']
        code_type=test_data['code_type']
        expected_code=test_data['expected_code']
        expected_msg=test_data['expected_msg']
        check_token = test_data["check_token"]

        code=self.correct_code if code_type=='correct' else  '9999'
        uuid=get_uuid['uuid']

        print()
        print(f"执行用例：{id} - {descripiton}")
        response=clinet.get_login(
            username=username,
            password=password,
            code=code,
            uuid=uuid
        )

        assert response.status_code==200
        data=response.json()
        #校验 code、msg
        if expected_code:
            assert data['code']==expected_code, \
                f"用例{id}失败，期望的code is:{expected_code},实际的code is:{data['code']} "

        if expected_msg:
            assert data['msg']==expected_msg, \
                f"用例{id}失败，期望的msg is:{expected_msg},实际的msg is:{data['msg']} "

        #登录成功才会有token的校验
        if check_token:
            assert "token" in data
            assert data["token"] is not None and data["token"] != ""
            print()
            print(f"{id}登录成功，token为:{data['token'][:20]}...")


    print(f"用例{id}通过！")
