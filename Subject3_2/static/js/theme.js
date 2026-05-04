function addPerson() {
    const container = document.getElementById("personContainer");

    // 새로운 사람 정보를 위한 입력 블록 생성
    const personBlock = document.createElement("div");
    personBlock.className = "person-block";
    personBlock.innerHTML = `
        <p>이름: <input type="text" name="name[]" required></p>
        <p>학과: <input type = "text" name = "Department[]" required></p>
        <p>학번: <input type="text" name="StudentNumber[]" required></p>
        <p>전화번호: <input type="text" name="phone[]" class="phone-input" placeholder="010-1234-5678" maxlength="13"></p>
        <p>이메일: <input type="text" name="mail[]" class="mail-input" placeholder="abc@gmail.com"></p>
    `;

    // 입력 블록을 personContainer에 추가
    container.appendChild(personBlock);
}