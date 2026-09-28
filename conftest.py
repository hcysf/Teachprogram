import  pytest
from src.dk_request import ReDate

#夹具 clint 客户端
@pytest.fixture(scope="function")
def clinet():
    client=ReDate()
    yield client
    client.close_session()

# 夹具获取验证码
@pytest.fixture(scope="function")
def get_uuid(clinet):
    response=clinet.get_captchaImage()
    assert response.status_code == 200
    data = response.json()
    return {"code":2,"uuid": data["uuid"]}

#夹具获取登录测试用例
@pytest.fixture(scope="function")
def test_login(clinet,get_uuid):
    code=get_uuid['code']
    uuid=get_uuid['uuid']
    response=clinet.get_login(username="admin",password="HM_2023_test",code=code,uuid=uuid)
    assert response.status_code==200
    data=response.json()
    assert "token" in data
    assert data["token"] is not None and data["token"] != ""
    print(f"登录成功!token为:{data['token'][:20]}...")
    clinet.set_token(data['token'])
    return clinet
#夹具创建新增课程，并且拿到其id的方法
@pytest.fixture(scope='function')
def add_course_id(test_login):
    import time
    name = f"测试课程_{int(time.time())}"
    response=test_login.add_course(
        name=name,
        subject="7",
        price=999,
        applicable_person="2",
        info="由fixture创建的测试课程")

    assert response.status_code==200
    data=response.json()
    assert data['code']==200,f"新增课程失败:{data["msg"]}"

    #通过课程名查询是否增加成功，并且拿到其id
    select_response=test_login.select_course(name=name)
    assert select_response.status_code==200
    list_data=select_response.json()

    if "id" in list_data["rows"][0] and len(list_data["rows"]) > 0:
        # 拿到索引为0的 课程id
        id = list_data["rows"][0]["id"]
        print(f"新增课程成功，id为：{id}")
        return id
    else:
        #查不到就主动让用例失败，并给出明确提示
        pytest.fail("无法获取创建课程id")


# #定义一个查询夹具
# @pytest.fixture(scope="function")
# def pytest_select_course(test_login,id):
#     response=test_login.get_course_by_id(course_id=id)
#     assert response.status_code==200
#     data=response.json()
#     return data
#
# #定义一个修改的夹具
# @pytest.fixture(scope="function")
# def pytest_updata_course(test_login,id):
#     response=test_login.update_course_by_id(course_id=id,
#                                             name="",
#                                             subject="",
#                                             price="",
#                                             applicable_person="",
#                                             info=""
#                                             )
#     assert response.status_cod==200
#     data=response.json()
#     return data
#
#
#
#
#
# #定义一个删除的夹具
# @pytest.fixture(scope="function")
# def pytest_delete_course(test_login,id):
#     response=test_login.delete_course_by_id(course_id=id)
#     assert response.status_code == 200
#     data = response.text()
#     assert data==200,"删除成功"









