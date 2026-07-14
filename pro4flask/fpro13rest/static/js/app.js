// ########################################################################################################
//                                          클라이언트 쪽
// ########################################################################################################

// 함수 (화살표함수) 객체 생성 후 $에 할당

// 현재 작업중인 객체를 선택하는 방법 -> 동적 선택
// function $(sel){
//     return document.querySelector(sel);
// }
const $ = (sel) => document.querySelector(sel);
// 예를 들어, $("#sendBtn") 하면, document.querySelector(sel)  실행


// 비동기 처리
$("#sendBtn").addEventListener("click", async() => {
    const name = $("#name").value.trim();
    // const age = $("#age").value.trim();

    // 기존 방식
    const age = document.querySelector("#age").value.trim();

    // key의 이름과 value가 동일하므로, name=name, age=age XX
    const params = new URLSearchParams({name, age});     // new URLSearchParams() : 공백, 한글이 포함된 경우, 자동 인코딩 : 홍길동 -> %ED%#787...
    const url = `/api/friend?${params.toString()}`;       // 최종 URL 생성 : /api/friend?name=길동&age=23     --> 사실, 한글 대신 인코딩된 문자열이 넘어감.

    $("#result").textContent = "요청 중 ...";           // 서버에 자료 요청 시간이 길어지면 보이는 메세지

    // Json 문자열을 Json 객체로 바꿔서 데이터를 클라이언트<->서버 에서 주고받음.
    try{
        // await : Ajax 요청을 기다림
        // 요청을 하고, 기다림.
        const res = await fetch(url, {
            method:"GET",
            headers:{"Accept":"application/json"}
        });
        
        // 요청을 받으면, Json 객체를 만듦.
        // 응답 본문을 json으로 파싱해서 JS 객체로 만듦.
        const data = await res.json();

        // 요청 실패한 경우
        // 성공하면 True(ok) / 실패하면 False
        if(!res.ok || data.ok === false){
            $("#result").innerHTML = `<span class="error">에러 : ${data.error}</span>`;
            return;

        }

        // 요청 성공인 경우 -> 데이터 출력
        $("#result").innerHTML = `
            <div>이름 : ${data.name}</div>
            <div>나이 : ${data.age}</div>
            <div>연령대 : ${data.age_group}</div>
            <div>메세지 : ${data.message}</div>
        `
    }catch(err){
        $("#result").innerHTML = `<span class="error">네트워크, 파싱 오류 : ${err}</span>`;
    }
});


