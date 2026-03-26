const btnJikwon = document.querySelector("#btnJikwon")
const btnOne = document.querySelector("#btnOne")
const btnBuser = document.querySelector("#btnBuser")
const btnDept = document.querySelector("#btnDept")

const jikwonno = document.querySelector("#jikwonno")
const buserno = document.querySelector("#buserno")

const msg = document.querySelector("#msg")
const thead = document.querySelector("#thead")
const tbody = document.querySelector("#tbody")

function setMsg(text){
    msg.textContent = text;
}

function clearTable(){
    thead.innerHTML = "";
    tbody.innerHTML = "";
}

function makeTable(rows){
    clearTable();

    if(!rows || rows.length === 0){
        setMsg("자료없음")
        return;
    }

    let header = "<tr>"

    Object.keys(rows[0]).forEach(key => {
        header += "<th>" + key + "</th>"
    })
    header += "</tr>";
    thead.innerHTML = header;

    rows.forEach(r => {
        let tr = "<tr>";
        Object.values(r).forEach(v => {
            tr += "<td>" + v + "</td>";
        });
        tr += "</tr>";
        tbody.innerHTML += tr;
    });
}

// 전체 직원
async function loadJikwon() {
    const res = await fetch("/api/jikwon")
    const mydata = await res.json();
    makeTable(mydata.data);

    setMsg("전체 직원 조회 완료")
}

// 직원 1명
async function loadOne() {
    const no = jikwonno.value;
    const res = await fetch("/api/jikwon/" + no)
    const data = await res.json();
    makeTable(data.data);

    setMsg("직원 1명 조회 완료")
}

// 전체 부서
async function loadBuser() {
    const res = await fetch("/api/buser")
    const bdata = await res.json();
    makeTable(bdata.data);

    setMsg("전체 부서 조회 완료")
}

// 부서 직원
async function loadDept() {
    const bno = buserno.value;
    const res = await fetch("/api/buser/" + bno + "/jikwon")
    const bdata = await res.json();
    makeTable(bdata.data);

    setMsg("특정 부서 직원 조회 완료")
}

btnJikwon.onclick = loadJikwon;
btnOne.onclick = loadOne;
btnBuser.onclick = loadBuser;
btnDept.onclick = loadDept;