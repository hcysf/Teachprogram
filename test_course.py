import  pytest
from  data.test_course import ADD_COURSE_TEST_DATA,QUERY_COURSE_TEST_DATA

class TestCourse:
    #新增课程
    #夹具参数化进行，数据驱动
    @pytest.mark.parametrize("test_course",ADD_COURSE_TEST_DATA)
    def test_add_course(self,test_login,test_course):
        id = test_course["id"]
        description = test_course["description"]
        course = test_course["course"]
        experience = test_course["experience"]
        check_exists = test_course.get("check_exists", False)

        print()
        print(f"{'=' * 50}")
        print(f"执行测试用例：{id}-{description}")
        print(f"请求参数：{course}")

        response=test_login.add_course(
            name=course["name"],
            subject=course["subject"],
            price=course["price"],
            applicable_person=course["applicable_person"],
            info=course["info"]
        )
        assert response.status_code==200
        data=response.json()

        # 校验msg、code
        assert data["code"] == experience["code"], \
            f"用例 {id} 失败: 期望 code={experience['code']}，实际 code={data['code']}"

        if "msg" in experience:
            assert data["msg"] == experience["msg"], \
                f"用例 {id} 失败: 期望 msg={experience['msg']}，实际 msg={data['msg']}"
        print(f"断言通过: code={data['code']}, msg={data['msg']}")

        #查询新增课程
        if check_exists and experience["code"] == 200:
            select_response=test_login.select_course(name=course["name"])
            select_data=select_response.json()
            assert select_data["code"] == 200
            assert len(select_data.get("rows", [])) > 0, \
                f"课程 '{course['name']}' 未在列表中找到"

            #校验查询的结果与新增的信息是否准确
            reslut_course = select_data["rows"][0]
            assert reslut_course["name"] == course["name"], \
                f"课程名称不匹配: {reslut_course['name']} != {course['name']}"
            assert reslut_course["price"] == course["price"], \
                f"课程价格不匹配: {reslut_course['price']} != {course['price']}"

            #校验课程是否存在
            course_id = reslut_course["id"]
            print(f"验证通过: 课程已存在，id={course_id}")
        print(f"用例 {id} 通过!")
        print("*"*70)
