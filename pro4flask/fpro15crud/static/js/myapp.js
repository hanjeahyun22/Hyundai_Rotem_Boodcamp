// 각종 요소
const code = document.querySelector("#code");
const sang = document.querySelector("#sang");
const su = document.querySelector("#su");
const dan = document.querySelector("#dan");

const msg = document.querySelector("#msg");
const tbody = document.querySelector("#tbody");

const btnAdd = document.querySelector("#btnAdd");
const btnUpdate = document.querySelector("#btnUpdate");
const btnDelete = document.querySelector("#btnDelete");
const btnReload = document.querySelector("#btnReload");


// 메세지 출력 함수
function setMsg(text){
    msg.textContent = text;
};

// 입력 폼 초기화 함수
function clearForm(){
    code. value = "";
    sang. value = "";
    su. value = "";
    dan. value = "";
};

// 전체 자료 읽는 함수
async function loadAll(){
    const res = await fetch("/api/sangdata");       // 방식 따로 안써주면 GET 방식
    const data = await res.json();
    // console.log(data);
    // alert(data);

    tbody.innerHTML = "";

    data.data.forEach(r => {
        // <tr> 태그 만들기
        const tr = document.createElement("tr");
        tr.innerHTML = "<td>" + r.code + "</td>" + 
                    "<td>" + r.sang + "</td>" + 
                    "<td>" + r.su + "</td>" + 
                    "<td>" + r.dan + "</td>";
        tbody.appendChild(tr);
    });

    clearForm();
    setMsg("조회 완료")
};

// 비동기 방식으로 데이터 추가
async function addData(){
    // alert("a")\
    const data = {
        // JavaScript에서 데이터 Dict type{Key:value}으로 생성
        code:Number(code.value),
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    };
    // alert(data);

    const res = await fetch("/api/sangdata", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(data)       // JSON모양의 JavaScript 객체를 문자열로 변환해 전송
    });

    // 받은 값으로 추가 작업을 하려는 경우
    //const imsi = await res.json();

    await res.json();
    setMsg("추가 완료");
    clearForm();
    loadAll();          // 추가 후 전체 자료 보기
};

async function updateData(){
    // alert("a")\
    const data = {
        // JavaScript에서 데이터 Dict type{Key:value}으로 생성
        // code:Number(code.value),             // 코드는 Primary Key이므로, 수정 XXXXXXXX
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    };
    // alert(data);

    const res = await fetch("/api/sangdata/" + code.value, {                // code.value 값을 반드시 줘야함. 있다고 가정.
        method:"PUT",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(data)       // JSON모양의 JavaScript 객체를 문자열로 변환해 전송
    });

    // 받은 값으로 추가 작업을 하려는 경우
    const imsi = await res.json();
    if(imsi.ok === true)  
        setMsg("수정 완료");
    else
        setMsg("수정 실패");

    clearForm();
    loadAll();          // 수정 후 전체 자료 보기
};

async function deleteData(){
    // alert("c")
    const res = await fetch("/api/sangdata/" + code.value, {                // code.value 값을 반드시 줘야함. 있다고 가정.
        method:"DELETE",
    });

    // 받은 값으로 추가 작업을 하려는 경우
    const imsi = await res.json();
    if(imsi.ok === true)  
        setMsg("imsi.msg");
    else
        setMsg("삭제 실패 : " + imsi.msg);

    clearForm();
    loadAll();          // 삭제 후 전체 자료 보기
};

window.onload = loadAll;

btnAdd.onclick = addData;
btnUpdate.onclick = updateData;
btnDelete.onclick = deleteData;
btnReload.onclick = loadAll;