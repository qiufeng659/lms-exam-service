from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据存储
exams = {
    "math_101": {
        "name": "Mathematics Exam",
        "questions": 10,
        "duration_minutes": 60
    },
    "python_101": {
        "name": "Python Programming Exam",
        "questions": 8,
        "duration_minutes": 45
    }
}

submissions = []


@app.route("/")
def home():
    "首页 - 服务状态检查"
    return {
        "service": "LMS Exam Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.route("/health")
def health():
    "健康检查接口"
    return {
        "status": "healthy",
        "timestamp": "2026-03-28T10:00:00Z"
    }


@app.route("/exams", methods=["GET"])
def list_exams():
    "获取所有考试列表"
    return jsonify({
        "exams": exams,
        "count": len(exams)
    })


@app.route("/exam/<exam_id>", methods=["GET"])
def get_exam(exam_id):
    "获取指定考试详情"
    if exam_id not in exams:
        return jsonify({"error": "Exam not found"}), 404

    return jsonify({
        "exam_id": exam_id,
        "details": exams[exam_id]
    })


@app.route("/exam/<exam_id>/submit", methods=["POST"])
def submit_exam(exam_id):
    """提交考试答案"""
    if exam_id not in exams:
        return jsonify({"error": "Exam not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    student_id = data.get("student_id")
    answers = data.get("answers")

    if not student_id or not answers:
        return jsonify({"error": "Missing student_id or answers"}), 400

    # 保存提交记录
    submission = {
        "submission_id": len(submissions) + 1,
        "exam_id": exam_id,
        "student_id": student_id,
        "answers": answers,
        "status": "submitted",
        "timestamp": "2026-03-28T10:00:00Z"
    }
    submissions.append(submission)

    return jsonify({
        "status": "success",
        "message": "Exam submitted successfully",
        "submission_id": submission["submission_id"]
    }), 201


@app.route("/submissions/<int:submission_id>", methods=["GET"])
def get_submission(submission_id):
    """获取提交记录"""
    for sub in submissions:
        if sub["submission_id"] == submission_id:
            return jsonify(sub)

    return jsonify({"error": "Submission not found"}), 404


@app.route("/submissions/student/<student_id>", methods=["GET"])
def get_student_submissions(student_id):
    """获取学生的所有提交记录"""
    student_subs = [sub for sub in submissions if sub["student_id"] == student_id]
    return jsonify({
        "student_id": student_id,
        "submissions": student_subs,
        "count": len(student_subs)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)