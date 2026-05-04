from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def input_page():
    # 사용자가 작성한 input.html 파일을 렌더링합니다.
    return render_template('input.html')

@app.route('/result', methods=['POST'])
def result():
    # 1. 일반 필드 리스트 가져오기
    names = request.form.getlist('name[]')
    departments = request.form.getlist('Department[]')
    student_numbers = request.form.getlist('StudentNumber[]')
    phones = request.form.getlist('phone[]')
    mail_ids = request.form.getlist('mail_id[]')
    mail_domains = request.form.getlist('mail_domain[]')

    # 2. 팀원별 데이터를 딕셔너리 리스트로 재구성
    team_members = []
    for i in range(len(names)):
        # 기술 스택은 tech_stack[0][], tech_stack[1][] 형태로 들어오므로 인덱스로 접근
        techs = request.form.getlist(f'tech_stack[{i}][]')
        
        member = {
            'name': names[i],
            'dept': departments[i],
            'sn': student_numbers[i],
            'phone': phones[i],
            'email': f"{mail_ids[i]}@{mail_domains[i]}",
            'techs': techs
        }
        team_members.append(member)

    # 3. 완성된 데이터를 result.html로 전달
    return render_template('result.html', members=team_members)

if __name__ == '__main__':
    app.run(debug=True, port=5000)