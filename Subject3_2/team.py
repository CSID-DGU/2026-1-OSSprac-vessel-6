from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 고정 팀원 정보: 서버를 껐다 켜도 바뀌지 않는 소개용 데이터입니다.
TEAM_MEMBERS = [
    {
        "name": "김태형",
        "dept": "통계학과",
        "phone": "010-9995-1234",
        "email": "teahyung@gmail.com",
        "role": "Team Leader / result.html 담당, 입력 정보를 결과 페이지에 출력하고 전체 웹사이트를 검토함.",
        "techs": ["Python", "Flask", "R", "GitHub", "JAVA", "SAS", "Linux"],
        "leader": True,
    },
    {
        "name": "권민재",
        "dept": "정보통신공학과",
        "phone": "010-6292-1234",
        "email": "minjae1234@gmail.com",
        "role": "input.html 담당, 팀원 정보 입력 폼과 기술 스택 선택 기능을 구현함.",
        "techs": ["C++", "JAVA", "Linux"],
        "leader": False,
    },
    {
        "name": "김종헌",
        "dept": "정보통신공학과",
        "phone": "010-2657-9037",
        "email": "jongheon371@gmail.com",
        "role": "contact.html 담당, 팀원 연락처 페이지와 카드형 UI를 구현함.",
        "techs": ["C++", "Python"],
        "leader": False,
    },
    {
        "name": "이영민",
        "dept": "건축학과",
        "phone": "010-8838-0140",
        "email": "lymin0106@gmail.com",
        "role": "index.html 담당, 팀 소개와 프로젝트 개요를 담은 메인 페이지를 구현함.",
        "techs": ["Python", "JAVA"],
        "leader": False,
    },
]
team_events = []

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/input")
def input_page():
    return render_template("input.html")


@app.route("/contact")
def contact():
    return render_template("contact.html", members=TEAM_MEMBERS)


@app.route("/result", methods=["POST"])
def result():
    names = request.form.getlist("name[]")
    departments = request.form.getlist("Department[]")
    student_numbers = request.form.getlist("StudentNumber[]")
    phones = request.form.getlist("phone[]")
    mail_ids = request.form.getlist("mail_id[]")
    mail_domains = request.form.getlist("mail_domain[]")

    submitted_members = []

    for i in range(len(names)):
        techs = request.form.getlist(f"tech_stack[{i}][]")

        if "etc" in techs:
            techs.remove("etc")
            etc_val = request.form.get(f"etc_stack[{i}]")
            if etc_val:
                etc_list = [t.strip() for t in etc_val.split(",") if t.strip()]
                techs.extend(etc_list)

        submitted_members.append(
            {
                "name": names[i],
                "dept": departments[i],
                "sn": student_numbers[i],
                "phone": phones[i],
                "email": f"{mail_ids[i]}@{mail_domains[i]}",
                "techs": techs,
            }
        )

    return render_template("result.html", members=submitted_members)

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(team_events)


@app.route('/api/events', methods=['POST'])
def add_event():
    data = request.get_json()

    title = data.get('title')
    date = data.get('date')
    time = data.get('time')
    member = data.get('member')
    memo = data.get('memo')
    event_type = data.get('type', 'meeting')

    if not title or not date:
        return jsonify({'error': '일정 제목과 날짜는 필수입니다.'}), 400

    event = {
        'id': len(team_events) + 1,
        'title': title,
        'date': date,
        'time': time,
        'member': member,
        'memo': memo,
        'type': event_type
    }

    team_events.append(event)

    return jsonify(event), 201


@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global team_events

    before_count = len(team_events)
    team_events = [event for event in team_events if event['id'] != event_id]

    if len(team_events) == before_count:
        return jsonify({'error': '해당 일정을 찾을 수 없습니다.'}), 404

    return jsonify({'message': '일정이 삭제되었습니다.'})

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()

    for event in team_events:
        if event['id'] == event_id:
            event['title'] = data.get('title', event['title'])
            event['date'] = data.get('date', event['date'])
            event['time'] = data.get('time', event.get('time', ''))
            event['type'] = data.get('type', event.get('type', 'meeting'))
            event['member'] = data.get('member', event.get('member', ''))
            event['memo'] = data.get('memo', event.get('memo', ''))
            return jsonify(event)

    return jsonify({'error': 'Event not found'}), 404

if __name__ == "__main__":
    # Docker 컨테이너 외부에서 접속 가능하도록 host='0.0.0.0' 설정
    app.run(host="0.0.0.0", debug=True, port=5000)