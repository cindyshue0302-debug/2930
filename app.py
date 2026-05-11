from flask import Flask, render_template, request

app = Flask(__name__)

# 從你的檔案中提取的測驗題目數據
quiz_data = [
    {
        "id": 1,
        "question": "「陣列」在存取某元素時，時間複雜度為何？",
        "options": ["A. O(1)", "B. O(n)", "C. O(log n)", "D. O(n^2)"],
        "answer": "A. O(1)"
    },
    {
        "id": 2,
        "question": "「陣列」是屬於下列何種資料結構？",
        "options": ["A. 動態", "B. 靜態", "C. 隨機", "D. 以上皆非"],
        "answer": "B. 靜態"
    },
    {
        "id": 3,
        "question": "若多項式的次數為 n，則使用 Horner’s Rule 的時間複雜度為何？",
        "options": ["A. O(1)", "B. O(n)", "C. O(n^2)", "D. O(log n)"],
        "answer": "B. O(n)"
    }
]

@app.route('/')
def index():
    return render_template('index.html', questions=quiz_data)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    results = []
    for q in quiz_data:
        user_answer = request.form.get(f"question_{q['id']}")
        is_correct = user_answer == q['answer']
        if is_correct:
            score += 1
        results.append({
            "question": q['question'],
            "user_answer": user_answer,
            "correct_answer": q['answer'],
            "is_correct": is_correct
        })
    return render_template('result.html', score=score, total=len(quiz_data), results=results)

if __name__ == '__main__':
    app.run(debug=True)