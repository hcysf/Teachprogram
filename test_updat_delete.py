import  random
import time
import  pytest

class TestUpdate:
    def test_update_course(self,test_login,add_course_id):
        course_id = add_course_id
        response = test_login.get_course_id(course_id)
        data = response.json()
        print(f"原始课程数据：{data}")


        name = f"{data["data"]["name"]}_{int(time.time())}"
        subject = str(random.randint(0,6))
        price = random.randint(1000,10000)
        info = f"测试_{int(time.time())}_信息"


        response_update = test_login.update_course_id(
            course_id=course_id,
            name=name,
            subject=subject,
            price=price,
            applicable_person=2,
            info=info,
        )


        assert response_update.status_code == 200, f"HTTP 请求失败: {response_update.status_code}"
        data_update = response_update.json()

        assert data_update["code"] == 200, f"更新失败：{data.get('msg')}"
        assert data_update["msg"] == "操作成功"

        #查看是否生效
        response_check = test_login.get_course_id(course_id)
        check_data = response_check.json()
        # 根据实际响应结构调整下面的断言
        # 假设返回的 data 中包含 id, name, price 等字段
        assert check_data["data"]["name"] == name, f"更新失败：当前名称是{check_data["data"][0]["name"]}"
        assert check_data["data"]["subject"] == subject, f"更新失败：当前名称是{check_data["data"][0]["subject"]}"
        assert check_data["data"]["price"] == price, f"更新失败：当前名称是{check_data["data"][0]["price"]}"
        assert check_data["data"]["info"] == info, f"更新失败：当前名称是{check_data["data"][0]["info"]}"

        print(f"更新后课程数据：{check_data}")
        print(f"课程 {course_id} 更新成功")


class TestDelete:

    def test_delete_course(self, test_login, add_course_id):

        course_id = add_course_id

        # 调用删除接口
        response_delete = test_login.delete_course_id(course_id)
        assert response_delete.status_code == 200
        data = response_delete.json()
        assert data["code"] == 200, f"删除失败：{data.get('msg')}"
        assert data["msg"] == "操作成功"

        # 再次查询，确认已删除
        response_check = test_login.get_course_id(course_id)
        check_data = response_check.json()

        assert check_data["code"] == 200, f"更新失败：当前名称是{check_data["msg"]}"
        assert check_data["msg"] == "操作成功"

        print(f"删除后查询结果：{check_data}")
        print(f"课程 {course_id} 删除成功")
