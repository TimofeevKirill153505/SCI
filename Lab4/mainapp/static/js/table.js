function generate(n) {
    hr = document.getElementById("hr")
    //alert(hr)
    table = document.createElement("table")
    table.setAttribute("id", "rand-table")
    for (i = 0; i < n; ++i) {
        tr = document.createElement("tr")
        for (j = 0; j < n; ++j) {
            td = document.createElement("td")
            td.textContent = Math.floor(Math.random() * 10);
            td.onclick = (event) => {
                curr = event.currentTarget
                cont = parseInt(curr.textContent)
                if (cont % 2 == 0) {
                    curr.style.backgroundColor = "red"
                }
                else {
                    curr.style.backgroundColor = "blue"
                }
            }
            tr.appendChild(td)
            //console.log("create td")
        }
        table.appendChild(tr)
    }
    //console.log("trying to insert before")
    hr.parentElement.insertBefore(table, hr)
}

//console.log(document.getElementById("generateTable"))

document.getElementById("generateTable").onclick = (event) => {
    if (document.getElementById("rand-table")) {
        //alert("removing table")
        document.getElementById("rand-table").parentElement.removeChild(document.getElementById("rand-table"))
    }
    n = parseInt(document.getElementById("tableN").value)
    //alert(n)
    generate(n)
}

document.getElementById("transpon").onclick = (event) => {
    if (!(document.getElementById("rand-table"))) return
    trs = $("#rand-table>tr")
    let size = trs.length
    arr = []
    for (let i = 0; i < size; ++i) {
        arr[i] = []
        let j = 0
        for (td of trs[i].children) {
            arr[i][j] = parseInt(td.textContent)
            //console.log(arr[i][j])
            ++j
        }
    }

    //console.log(arr);

    for (let i = 0; i < size; ++i) {
        let j = 0
        for (td of trs[i].children) {
            td.textContent = arr[j][i]
            //console.log(arr[j][i])
            ++j
        }
    }
}