$(function () {
    document.getElementsByName("background")[0].onchange = (event) => {
        $("#background-form").toggle()
    }
    document.getElementById("changeBackgroundColor").onclick = (event) => {
        console.log("in button event");
        obj = { r: 0, g: 0, b: 0, a: 0 }
        for (element of $("#background-form > input")) {
            console.log("name " + $(element).prop("name"));
            console.log("value " + element.value);
            obj[$(element).prop("name")] = element.value
        }

        //console.log("new background color " + obj.r + " " + obj.g + " " + obj.b + " " + obj.a);
        $("body").css("background-color", `rgba(${obj.r}, ${obj.g},${obj.b},${obj.a})`)
    }

    document.getElementById("defaultColor").onclick = (event) => {
        $("body").css("background-color", `rgba(255, 255,255,255)`)
    }

    document.getElementsByName("fontcolor")[0].onchange = (event) => {
        $("#fontcolor-form").toggle()
    }

    document.getElementById("changeFontColor").onclick = (event) => {
        console.log("in button event");
        obj = { r: 0, g: 0, b: 0, a: 0 }
        for (element of $("#fontcolor-form > input")) {
            console.log("name " + $(element).prop("name"));
            console.log("value " + element.value);
            obj[$(element).prop("name")] = element.value
        }

        //console.log("new background color " + obj.r + " " + obj.g + " " + obj.b + " " + obj.a);
        $("body").css("color", `rgba(${obj.r}, ${obj.g},${obj.b})`)
    }
    document.getElementById("defaultFontColor").onclick = (event) => {
        $("body").css("color", `rgb(0, 0, 0)`)
    }

    document.getElementsByName("fontsize")[0].onchange = (event) => {
        if (event.target.checked) {
            //console.log(`e t v ${event.target.checked}`);
            inp = document.createElement("input")
            inp.setAttribute("type", 'number')
            inp.setAttribute("id", 'fontsize-input')
            inp.setAttribute("max", '30')
            inp.setAttribute("min", '9')
            inp.setAttribute("value", '16')
            document.getElementsByName("fontsize")[0].parentElement.appendChild(inp)
            btn1 = document.createElement("button")
            btn1.setAttribute("type", 'button')
            btn1.setAttribute("id", 'btn1')
            btn1.textContent = "Применить"
            btn1.onclick = (event) => {
                console.log(`onclick btn1 ${document.getElementById("fontsize-input").value}`);
                $("body").css("font-size", `${document.getElementById("fontsize-input").value}px`)

            }
            document.getElementsByName("fontsize")[0].parentElement.appendChild(btn1)
            btn1 = document.createElement("button")
            btn1.setAttribute("type", 'button')
            btn1.setAttribute("id", 'btn2')
            btn1.onclick = (event) => {
                $("body").prop("font-size", 16)
            }
            btn1.textContent = "Сбросить"
            document.getElementsByName("fontsize")[0].parentElement.appendChild(btn1)
        }
        else {
            parent = document.getElementById("btn1").parentElement
            parent.removeChild(document.getElementById("btn1"))
            parent.removeChild(document.getElementById("fontsize-input"))
            parent.removeChild(document.getElementById("btn2"))
        }
    }
})