const $ = (sel) => document.querySelector(sel); 

// DOM 요소들을 한 번에 찾아 변수(객체)에 담아두고, 이후에 편하게 쓰려고 만든 요소 캐싱 패턴.
// els는 각 DOM 요소를 key-value로 모아 둔 객체 변수명. els.code, els.sang 이렇게 호출
const els = {
    code: $("#code"), 
    sang: $("#sang"), 
    su: $("#su"), 
    dan: $("#dan"),
    msg: $("#msg"),
    tbody: $("#tbody"),
    btnAdd: $("#btnAdd"), btnUpdate: $("#btnUpdate"), btnDelete: $("#btnDelete"), 
    btnClear: $("#btnClear"),
    btnReload: $("#btnReload"),
};

// <div id="msg" class="msg">메시지 영역</div>에 메세지 출력용 함수
function setMsg(text, isError = false) {
    els.msg.textContent = text;
    els.msg.classList.toggle("error", isError);   // msg 요소에 error 클래스를 조건에 따라 붙이거나 뗌
        // classList.toggle(클래스명, 조건) 형태는
        // 조건이 true면 → 해당 클래스를 추가(add), 조건이 false면 → 해당 클래스를 제거(remove)
}

function getForm() {
    return {
        code: els.code.value.trim(),
        sang: els.sang.value.trim(),
        su: els.su.value.trim(),
        dan: els.dan.value.trim(),
    };
}

function clearForm() {
    els.code.value = "";
    els.sang.value = "";
    els.su.value = "";
    els.dan.value = "";
    setMsg("초기화 완료");
}

// 서버에서 받은 상품 목록(rows)을 tr로 만들어서 테이블 tbody에 한 번에 뿌려주는 함수
// 결과는 [ "<tr ...>...</tr>", "<tr ...>...</tr>", ... ]
function renderRows(rows) {
    els.tbody.innerHTML = rows.map(r => `
        <tr data-code="${r.code}">
        <td>${r.code}</td>
        <td>${r.sang ?? ""}</td>
        <td>${r.su ?? ""}</td>
        <td>${r.dan ?? ""}</td>
        </tr>` ).join("");
}
// <tr data-code="${r.code}"> : tr(한 행)에 data-code="1" 같은 커스텀 데이터 속성을 달아둔다.
// 나중에 '행 클릭했을 때 code를 쉽게 꺼내기'에 좋음. 예: tr.dataset.code 로 읽음

// async : 이 함수 안에서 await를 쓸 수 있게 해주는 표시임. 이 함수는 호출하면 즉시 Promise를 반환
async function loadAll() {
    setMsg("조회 중...");
    try {
    // 서버 API로 GET 요청을 보내고, 응답이 올 때까지 기다린 다음 그 응답 객체를 res에 담는 코드
    // fetch()는 HTTP 요청을 보내는 브라우저 내장 함수
    // window.API_LIST는 index.html에서 주입한 API 주소:<script>window.API_LIST = ...</script>
    // 아래 코드를 통해 브라우저가 GET /api/sangdata 요청을 보냄
        const res = await fetch(window.API_LIST, { headers: { "Accept": "application/json" } });

        // 서버 응답(res)의 본문(body)을 “JSON으로 읽어서” 자바스크립트 객체로 변환.
        const data = await res.json();
        if (!res.ok || data.ok === false) throw new Error(data.error || "조회 실패");

        renderRows(data.data);  // tbody에 결과 출력 함수 호출
        setMsg(`조회 완료: ${data.data.length}건`);
    } catch (e) {
        setMsg(`조회 오류: ${e.message}`, true);
    }
}

// 추가
async function addOne() {
    const f = getForm();   // form tag의 입력된 자료 읽기 함수 호출
    if (!f.code || !f.sang) return setMsg("code, sang는 필수!", true);
    try {
        const res = await fetch(window.API_LIST, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify( {    // stringify : JS 객체/배열을 JSON 문자열로 변환
            code: Number(f.code),
            sang: f.sang,
            su: Number(f.su || 0),
            dan: Number(f.dan || 0),
        } )
        } );
        
        // HTTP 응답(res)의 본문(body)을 끝까지 읽어서 JSON으로 파싱한 뒤, 그 결과가 나올 때까지 대기
        const data = await res.json();
        if (!res.ok || data.ok === false) throw new Error(data.error || "추가 실패");

        setMsg(`추가 완료: code=${data.code}`);
        await loadAll();   // loadAll()이 반환하는 Promise가 resolve/reject 될 때까지 대기.
    } catch (e) {
        setMsg(`추가 오류: ${e.message}`, true);
    }
}

// 수정
async function updateOne() {
    const f = getForm();
    if (!f.code) return setMsg("수정하려면 code가 필요!", true);

    try {
        const res = await fetch(`${window.API_LIST}/${Number(f.code)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify( {
            sang: f.sang,
            su: Number(f.su || 0),
            dan: Number(f.dan || 0),
        })
        } );
        const data = await res.json();
        if (!res.ok || data.ok === false) throw new Error(data.error || "수정 실패");

        setMsg(`수정 완료: code=${data.code}`);
        await loadAll();
    } catch (e) {
        setMsg(`수정 오류: ${e.message}`, true);
    }
}

// 삭제
async function deleteOne() {
    const f = getForm();
    if (!f.code) return setMsg("삭제하려면 code가 필요!", true);

    if (!confirm(`code=${f.code}를 삭제할까요?`)) return;

    try {
        const res = await fetch(`${window.API_LIST}/${Number(f.code)}`, {
        method: "DELETE",
        headers: { "Accept": "application/json" }
        });
        const data = await res.json();
        if (!res.ok || data.ok === false) throw new Error(data.error || "삭제 실패");

        setMsg(`삭제 완료: code=${data.code}`);
        clearForm();
        await loadAll();
    } catch (e) {
        setMsg(`삭제 오류: ${e.message}`, true);
    }
}

// 행 클릭 → 폼 채우기
els.tbody.addEventListener("click", (e) => {
  // 클릭된 위치에서 가장 가까운(자기 자신 포함) 조상 요소 중 <tr>(테이블 행)을 찾는 코드
    const tr = e.target.closest("tr");   
    if (!tr) return;
    const tds = tr.querySelectorAll("td");
    els.code.value = tds[0].textContent;
    els.sang.value = tds[1].textContent;
    els.su.value = tds[2].textContent;
    els.dan.value = tds[3].textContent;
    setMsg(`선택됨: code=${els.code.value}`);
});

// 버튼 이벤트 장착
els.btnReload.addEventListener("click", loadAll);
els.btnClear.addEventListener("click", clearForm);
els.btnAdd.addEventListener("click", addOne);
els.btnUpdate.addEventListener("click", updateOne);
els.btnDelete.addEventListener("click", deleteOne);

// 최초 로딩 시 전체조회
window.addEventListener("DOMContentLoaded", loadAll);

