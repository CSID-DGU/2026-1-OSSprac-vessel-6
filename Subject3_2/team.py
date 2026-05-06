from flask import Flask, render_template, request

app = Flask(__name__)
saved_members = []
'''
index -> input -> result 순서로 진행하기 위해 기존 코드를 주석처리 하였습니다.
@app.route('/')
def input_page():
    # 사용자가 작성한 input.html 파일을 렌더링합니다.
    return render_template('input.html')
'''
@app.route('/') # 1. index
def main():
    return render_template('index.html')

@app.route('/input') # 2. input
def input_page():
    return render_template('input.html')

added_members = []

@app.route('/contact')
def contact_page():
    # 1. 고정된 팀장 정보
    team_leader = {
        "name": "김태형",
        "dept": "통계학과",
        "phone": "010-9995-1234",
        "email": "teahyung@gmail.com",
        "techs": ["Python", "Flask", "R", "GitHub","JAVA","SAS","Linux"],
        "description": "result.html 담당,  input에 입력한 정보를 출력하는 result 페이지를 구현하였음. 웹사이트를 구현하는 과정에서 팀원들이 업로드한 html 파일들을 수정하는 등 웹사이트를 최종적으로 검토하였음."
    }

    # 2. 처음부터 들어있는 고정 팀원 정보
    default_members = [
        {
            "name": "권민재",
            "dept": "정보통신공학과",
            "phone": "010-6292-1234",
            "email": "minjae1234@gmail.com",
            "techs": ["C++", "JAVA","Linux"],
            "description": "input.html 담당, 이름,학과,학번,전화번호,이메일,기술스택 입력칸을 구현하였음. 기술스택 입력칸은 기타를 선택할 경우 텍스트 입력칸이 나타나도록 구현하였음. 또한 style.css, theme.js도 같이 구현하였음."
        },
        {
            "name": "김종헌",
            "dept": "정보통신공학과",
            "phone": "010-2657-9037",
            "email": "jongheon371@gmail.com",
            "techs": ["C++", "Python"],
            "description": "contact.html 담당, 팀원들의 정보를 보여주는 contact.html을 구현하였음. 이 과정에서 style.css, theme.js도 같이 구현하였음."
        },
        {
            "name": "이영민",
            "dept": "건축학과",
            "phone": "010-8838-0140",
            "email": "lymin0106@gmail.com",
            "techs": ["Python", "JAVA"],
            "description": "index.html 담당, 팀의 소개와 프로젝트의 개요를 담은 index.html을 구현하였음. AOS 라이브러리를 활용하여 애니메이션 효과를 추가하였고, 다크모드도 구현하였음. 또한 style.css, theme.js도 같이 구현하였음."
        }
    ]

    # 고정 팀원과 input으로 추가된 팀원을 합칩니다.
    all_members = default_members + added_members

    return render_template('contact.html', leader=team_leader, members=all_members)

@app.route('/result', methods=['POST']) # 3. result
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
        
        if 'etc' in techs:
            techs.remove('etc') # 'etc'라는 글자 자체는 제거
            etc_val = request.form.getlist('etc_stack[]')[i]
            if etc_val:
                # 쉼표로 구분해서 입력했을 경우를 대비해 분리하여 추가
                etc_list = [t.strip() for t in etc_val.split(',') if t.strip()]
                techs.extend(etc_list)
        
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
    added_members.extend(team_members)
    return render_template('result.html', members=team_members)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
