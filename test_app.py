import unittest
import json
from app import app, submissions


class TestLMSExamService(unittest.TestCase):

    def setUp(self):
        """每个测试前运行"""
        self.client = app.test_client()
        app.config['TESTING'] = True

        submissions.clear()

    def test_home_endpoint(self):
        """测试首页接口"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['service'], 'LMS Exam Service')
        self.assertEqual(data['status'], 'running')
        self.assertEqual(data['version'], '1.0.0')
        print("Тест главной страницы пройден")

    def test_health_endpoint(self):
        """测试健康检查接口"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        print("Медицинский осмотр пройден.")

    def test_list_exams(self):
        """测试获取考试列表"""
        response = self.client.get('/exams')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('exams', data)
        self.assertEqual(data['count'], 2)  # 预定义了2个考试
        self.assertIn('math_101', data['exams'])
        self.assertIn('python_101', data['exams'])
        print("Список экзаменационных работ, тест пройден.")

    def test_get_specific_exam(self):
        """测试获取指定考试"""
        # 测试存在的考试
        response = self.client.get('/exam/math_101')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['exam_id'], 'math_101')
        self.assertEqual(data['details']['name'], 'Mathematics Exam')
        self.assertEqual(data['details']['questions'], 10)

        # 测试不存在的考试
        response = self.client.get('/exam/unknown')
        self.assertEqual(response.status_code, 404)
        print("Сдать указанный экзамен")

    def test_submit_exam(self):
        """测试提交考试"""
        submission_data = {
            "student_id": "student_001",
            "answers": {
                "q1": "5",
                "q2": "4",
                "q3": "3",
                "q3": "2"
            }
        }

        response = self.client.post('/exam/math_101/submit',
                                    json=submission_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['submission_id'] >= 1)
        print("Отправьте экзаменационный бланк и сдайте тест")

    def test_submit_exam_invalid_data(self):
        """测试提交考试 - 无效数据"""
        # 缺少student_id
        response = self.client.post('/exam/math_101/submit',
                                    json={"answers": {}},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # 缺少answers
        response = self.client.post('/exam/math_101/submit',
                                    json={"student_id": "student_001"},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        print("Проверка на недопустимые данные пройдена")

    def test_get_submission(self):
        """测试获取提交记录"""
        # 先提交一个考试
        submission_data = {
            "student_id": "student_002",
            "answers": {"q1": "5", "q2": "3"}
        }
        self.client.post('/exam/math_101/submit', json=submission_data)

        # 获取提交记录
        response = self.client.get('/submissions/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['student_id'], 'student_002')
        self.assertEqual(data['exam_id'], 'math_101')
        self.assertEqual(data['status'], 'submitted')
        print("Проверка на получение истории коммитов пройдена успешно")

    def test_get_student_submissions(self):
        """测试获取学生所有提交"""
        # 提交多个考试
        student_id = "student_003"

        self.client.post('/exam/math_101/submit',
                         json={"student_id": student_id, "answers": {"q1": "5"}})
        self.client.post('/exam/python_101/submit',
                         json={"student_id": student_id, "answers": {"q1": "3"}})

        # 获取学生提交记录
        response = self.client.get(f'/submissions/student/{student_id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['student_id'], student_id)
        self.assertEqual(data['count'], 2)
        print("Тест получения записей о сдачах студента пройден")


if __name__ == '__main__':

    unittest.main(verbosity=2)