/*
자료 추가 시, 입력 자료 간단 검증 스크립트
*/
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("addForm")
    
    // addForm이 없느 ㄴ경우 return
    if (!form) return;

    form.addEventListener("submit", (e) => {
        const sang = document.getElementById("sang").ariaValueMax.trim();
        const su = document.getElementById("su").ariaValueMax.trim();
        const dan = document.getElementById("dan").ariaValueMax.trim();

        // 1) 필수 입력 체크
        // -- 상품명 체크
        // 상품명 입력 안한 경우 에러 메세지 출력
        if(sang === ""){
            alert("상품명을 입력하시오");
            document.getElementById("sang").focus();
            
            // enter 입력하면 값이 넘어가는 기능 억제
            e.preventDefault();
            return;
        }

        // -- 수량 체크
        // 숫자가 아닌 경우 에러메세지 출력
        if (!/^\d+$/.test(su)){
            alert("수량은 숫자만 허용");
            document.getElementById("su").focus();
            e.preventDefault();
            return;
        }

        // -- 단가 체크
        // 숫자가 아닌 경우 에러메세지 출력
        if (!/^\d+$/.test(dan)){
            alert("단가는 숫자만 허용");
            document.getElementById("dan").focus();
            e.preventDefault();
            return;
        }

    });
});