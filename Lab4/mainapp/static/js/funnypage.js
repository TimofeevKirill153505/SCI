$(function () {
    //console.log("on ready func")
    $(".cards-wrapper .card").each((index, elem) => {
        //console.log("added eventListener")
        //$(elem).css("background-color", "red")
        elem.addEventListener("mousemove", onMousemove(elem))
    })

    for (element of document.getElementsByClassName("card")) {
        //console.log("add mouseLeave listeners")
        $(element).bind("mouseleave", onMouseleave(element))
    };

    window.addEventListener("scroll", (event) => {

        moveLeft($(".red-square.left")[0], 2)
        moveLeft($(".white-square.left")[0], 1)
        moveRight($(".white-square.right")[0], 1)
        moveRight($(".red-square.right")[0], 2)
    })


})

function onMousemove(card) {
    return function (mouseEvent) {
        //console.log("in eventListener")
        //console.log(card_w.getBoundingClientRect());
        const [x, y] = [mouseEvent.offsetX, mouseEvent.offsetY];
        const rect = card.getBoundingClientRect();
        const [width, height] = [rect.width, rect.height];
        const middleX = width / 2;
        const middleY = height / 2;
        const offsetX = ((x - middleX) / middleX) * 40;
        const offsetY = ((y - middleY) / middleY) * 40;
        // const offX = 50 + ((x - middleX) / middleX) * 25;
        // const offY = 50 - ((y - middleY) / middleY) * 20;
        card.style.setProperty("--rotateX", 1 * offsetX + "deg");
        card.style.setProperty("--rotateY", -1 * offsetY + "deg");
        // card.style.setProperty("--posx", offX + "%"); // эти свойства для бэкграунда
        // card.style.setProperty("--posy", offY + "%");
    }
}

function onMouseleave(card) {

    return function (mouseEvent) {
        //console.log("in leave event");
        card.style.setProperty("--rotateX", 0 + "deg");
        card.style.setProperty("--rotateY", 0 + "deg");
    }
}

function moveRight(element, speed) {
    //console.log("moveleft" + element);
    y = document.defaultView.window.scrollY

    //console.log("Смещение для амогусов " + thing + "px")

    $(element).css("left", speed * y + "px")
}

function moveLeft(element, speed) {
    //console.log("moveleft" + element);
    y = document.defaultView.window.scrollY
    //console.log("lalaLA" + speed * y + "px")
    $(element).css("right", speed * y + "px")
}