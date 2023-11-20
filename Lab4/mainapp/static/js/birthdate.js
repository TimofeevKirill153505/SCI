$(function () {
    $("#modal").show()
    today = new Date()
    document.getElementById("birthdate-input").value = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
    //alert(`${today.getFullYear()}-${today.getMonth()}-${today.getDay()}`)
    document.getElementById("birthdate-button").addEventListener("click", (event) => {
        //alert("in click event")
        //alert(`in input ${document.getElementById("birthdate-input").value}`)
        $("#modal").hide()
        console.log("click event");

        date = new Date(document.getElementById("birthdate-input").value)
        if (!((today.getFullYear() - date.getFullYear() >= 18) && (today.getMonth() - date.getMonth() >= 0
            || (today.getMonth() - date.getMonth() == 0 && today.getDate() - date.getDate() >= 0)))) {
            alert("Вам нет 18!!!")

        }
        //alert(`years ${today.getFullYear() - date.getFullYear()} months ${today.getMonth() - date.getMonth()}  days${today.getDate() - date.getDate() >= 0} `)
    })
    //console.log($("#modal"));
})