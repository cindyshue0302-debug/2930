from flask import Flask, render_template, request

app = Flask(__name__)

# 你的 22 題完整題庫
QUESTIONS = [
    {
        "id": 1,
        "question": "「陣列」是屬於下列何種資料結構？",
        "options": ["A. 線性", "B. 靜態", "C. 動態", "D. 以上皆非"],
        "answer": "B",
        "desc": "陣列是一種靜態資料結構，其大小在建立時即固定，且在記憶體中佔用連續空間。"
    },
    {
        "id": 2,
        "question": "承上題，若是「以行為主」的記憶體配置，則 A[1][2] 的位址為何？",
        "options": ["A. 1012", "B. 1016", "C. 1024", "D. 1020", "E. 以上皆非"],
        "answer": "E",
        "desc": "以行為主 (Column-major) 計算公式為：Base + (j * Num_Rows + i) * Size。1000 + (2 * 3 + 1) * 4 = 1028。因 1028 不在選項中，故選 E。"
    },
    {
        "id": 3,
        "question": "若某「一維陣列」的長度為 100，每個元素需要 4 個位元組 (bytes)，則儲存這個陣列共需多少位元組 (bytes)？",
        "options": ["A. 100", "B. 200", "C. 400", "D. 800"],
        "answer": "C",
        "desc": "總位元組數 = 陣列長度 × 元素大小 = 100 × 4 = 400 bytes。"
    },
    {
        "id": 4,
        "question": "「陣列」在存取某元素時，時間複雜度為何？",
        "options": ["A. O(1)", "B. O(log n)", "C. O(n)", "D. O(n^2)"],
        "answer": "A",
        "desc": "陣列可透過索引（Index）直接計算出記憶體位址，存取時間為常數時間 O(1)。"
    },
    {
        "id": 5,
        "question": "若某「二維陣列」A的維度為 3*3，物理位址為 1,000，每個元素均為整數，需要 4 個位元組 (bytes) 儲存。若是「以列為主」的記憶體配置，則 A[1][2] 的位址為何？",
        "options": ["A. 1008", "B. 1012", "C. 1016", "D. 1020"],
        "answer": "D",
        "desc": "以列為主 (Row-major) 計算公式為：Base + (i * Num_Cols + j) * Size。1000 + (1 * 3 + 2) * 4 = 1020。"
    },
    {
        "id": 6,
        "question": "「魔術方塊」（幻方）的特性為何？",
        "options": ["A. 列的總和不等於行的總和", "B. 列、行或對角線的總和都相等", "C. 魔術方塊內的數字必須互不相同且大於100", "D. 魔術方塊內的數字均為奇數"],
        "answer": "B",
        "desc": "魔術方塊（幻方）的定義即為每行、每列以及主對角線上的數字和均相等。"
    },
    {
        "id": 7,
        "question": "某農夫有一個籠子，裡面有雞和兔子。已知總共有 30 隻，且總共有 80 隻腳。請問籠子裡有幾隻兔子？",
        "options": ["A. 10", "B. 15", "C. 20", "D. 25"],
        "answer": "A",
        "desc": "設兔子 R 隻，雞 (30-R) 隻。4R + 2(30-R) = 80 => 2R + 60 = 80 => R = 10。"
    },
    {
        "id": 8,
        "question": "「矩陣乘法」的演算法中包含三個嵌套迴圈（Nested Loops），則其時間複雜度為何？",
        "options": ["A. O(n)", "B. O(n log n)", "C. O(n^2)", "D. O(n^3)"],
        "answer": "D",
        "desc": "傳統矩陣乘法由三個從 0 到 n-1 的迴圈巢狀組成，因此時間複雜度為 O(n³)。"
    },
    {
        "id": 9,
        "question": "請問「騎士巡邏」問題的目的為何？",
        "options": ["A. 找到一條最快吃掉對方國王的路徑", "B. 找到一條路徑，從出發點開始，每個格子只能走訪一次，且所有的格子都走訪完"],
        "answer": "B",
        "desc": "騎士巡邏（Knight's Tour）要求騎士不重複地走遍棋盤上每一個格子恰好一次。"
    },
    {
        "id": 10,
        "question": "考慮 n*n 的棋盤，則「騎士巡邏」問題的可能解有幾種？",
        "options": ["A. 只有一種", "B. n 種", "C. 無窮多種", "D. 不一定，視騎士的出發點而定"],
        "answer": "D",
        "desc": "騎士巡邏問題的解法數量取決於棋盤大小 n 以及騎士的起始位置，甚至某些起點可能無解。"
    },
    {
        "id": 11,
        "question": "考慮下列的多項式：p1(x) = 3x^3 + 2x^2 - x + 5, p2(x) = x^3 - 4x^2 + 2x - 3，則多項式加法 p1(x) + p2(x) 的結果為何？",
        "options": ["A. 4x^3 + 2x^2 + x + 2", "B. 4x^3 - 2x^2 - x + 2", "C. 4x^3 - 2x^2 + x + 2", "D. 4x^3 + 6x^2 + x + 8"],
        "answer": "C",
        "desc": "同次項係數相加：(3+1)x³ + (2-4)x² + (-1+2)x + (5-3) = 4x³ - 2x² + x + 2。"
    },
    {
        "id": 12,
        "question": "若多項式的最高次數為 n，則 Horner's Rule（秦九韶算法）的時間複雜度為何？",
        "options": ["A. O(1)", "B. O(n)", "C. O(n^2)", "D. O(2^n)"],
        "answer": "B",
        "desc": "Horner's Rule 通過提公因式，將多項式求值簡化為 n 次乘法和 n 次加法，時間複雜度為 O(n)。"
    },
    {
        "id": 13,
        "question": "「鏈結串列」（Linked List）中，每個節點（Node）除了儲存資料外，還必須儲存什麼？",
        "options": ["A. 索引值", "B. 指向下一個節點的指標 (Pointer/Link)", "C. 陣列的長度", "D. 記憶體的初始位址"],
        "answer": "B",
        "desc": "單向鏈結串列的節點包含「資料欄位（Data）」與指向下一節點的「指標欄位（Link/Next）」。"
    },
    {
        "id": 14,
        "question": "在「單向鏈結串列」中插入或刪除一個節點的時間複雜度（已知目標位置）為何？",
        "options": ["A. O(1)", "B. O(log n)", "C. O(n)", "D. O(n^2)"],
        "answer": "A",
        "desc": "若已指明插入或刪除的位置，只需調整指標的指向，時間複雜度為 O(1)。"
    },
    {
        "id": 15,
        "question": "「堆疊」（Stack）資料結構遵循下列哪一種存取原則？",
        "options": ["A. FIFO (First-In, First-Out)", "B. LIFO (Last-In, First-Out)", "C. LILO (Last-In, Last-Out)", "D. 隨機存取"],
        "answer": "B",
        "desc": "堆疊是後進先出（Last-In, First-Out）的資料結構，如同疊盤子，最後放上去的先拿走。"
    },
    {
        "id": 16,
        "question": "「佇列」（Queue）資料結構遵循下列哪一種存取原則？",
        "options": ["A. FIFO (First-In, First-Out)", "B. LIFO (Last-In, First-Out)", "C. FILO (First-In, Last-Out)", "D. 隨機存取"],
        "answer": "A",
        "desc": "佇列是先進先出（First-In, First-Out）的資料結構，如同排隊，先排隊的人先離開。"
    },
    {
        "id": 17,
        "question": "在堆疊（Stack）中，將資料放入堆疊的操作稱為什麼？",
        "options": ["A. Pop", "B. Push", "C. Insert", "D. Enqueue"],
        "answer": "B",
        "desc": "堆疊放入資料的操作稱為 Push（推入），取出資料的操作稱為 Pop（彈出）。"
    },
    {
        "id": 18,
        "question": "若將表達式 `(A + B) * C` 轉換為「後序式」（Postfix），結果為何？",
        "options": ["A. +AB*C", "B. AB+C*", "C. ABC*+", "D. *+ABC"],
        "answer": "B",
        "desc": "括號內先處理：(A + B) 轉為 AB+。接著與 C 相乘：AB+ C *，即為 AB+C*。"
    },
    {
        "id": 19,
        "question": "二元樹（Binary Tree）中，一個節點最多可以有幾個子節點（Children）？",
        "options": ["A. 1 個", "B. 2 個", "C. 3 個", "D. 無限制"],
        "answer": "B",
        "desc": "二元樹的定義為每個節點的分支度（Degree）最大不超過 2，即最多只有 2 個子節點。"
    },
    {
        "id": 20,
        "question": "一棵高度為 h 的滿二元樹（Full Binary Tree），其總節點數為多少？",
        "options": ["A. 2^h", "B. 2^h - 1", "C. 2^(h-1)", "D. h^2"],
        "answer": "B",
        "desc": "高度為 h 的滿二元樹，節點總數公式為 2^h - 1。"
    },
    {
        "id": 21,
        "question": "若對二元樹進行「中序走訪」（Inorder Traversal），走訪順序為何？",
        "options": ["A. 左子樹 -> 根節點 -> 右子樹", "B. 根節點 -> 左子樹 -> 右子樹", "C. 左子樹 -> 右子樹 -> 根節點", "D. 根節點 -> 右子樹 -> 左子樹"],
        "answer": "A",
        "desc": "中序走訪順序為：先走訪左子樹，再拜訪根節點，最後走訪右子樹（L-D-R）。"
    },
    {
        "id": 22,
        "question": "若多項式的次數為 n，則 Horner’s Rule 的時間複雜度為何？",
        "options": ["A. O(1)", "B. O(n)", "C. O(n^2)", "D. O(2^n)", "E. 以上皆非"],
        "answer": "B",
        "desc": "Horner's Rule 的時間複雜度為 O(n)，重複確認本題的核心考點。"
    }
]

@app.route('/')
def index():
    return render_template('index.html', questions=QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    results = []
    
    for q in QUESTIONS:
        user_ans = request.form.get(f"q_{q['id']}")
        # 取得選項中的英文字母 A, B, C, D
        user_letter = user_ans.split('.')[0].strip() if user_ans else "未作答"
        
        is_correct = (user_letter == q['answer'])
        if is_correct:
            score += 1
            
        results.append({
            "id": q['id'],
            "question": q['question'],
            "user_ans": user_ans if user_ans else "未作答",
            "correct_ans": q['answer'],
            "is_correct": is_correct,
            "desc": q['desc']
        })
        
    return render_template('result.html', score=score, total=len(QUESTIONS), results=results)

if __name__ == '__main__':
    app.run(debug=True)