var time = 5000

var img_arr = ["banner.jpg", "banner2.jpg"]
var refs = ["https://vk.com", "https://youtube.com"]

curr_img = 0
curr_img_bl = 0

$(function () {
    //console.log("in jquery thing")
    setTimeout(rotation_func, time)
})

function rotation_func() {
    //console.log("in rotation func")
    frst = $("div.banner > a > img")[curr_img_bl]
    scnd = $("div.banner > a > img")[(curr_img_bl + 1) % 2]

    $(scnd).prop("src", "../static/" + img_arr[(curr_img + 1) % img_arr.length])
    //$(scnd).prop("opacity", 0)

    $(scnd).animate({ opacity: 1 }, {
        duration: 1000,
        complete: function () {
        }
    })

    $(frst).animate({ opacity: 0 }, {
        duration: 1000,
        complete: function () {
            $("div.banner > a")[0].setAttribute("href", refs[curr_img])
        }
    })
    //console.log("done with rotation things")
    curr_img += 1
    curr_img %= img_arr.length
    curr_img_bl += 1
    curr_img_bl %= 2
    //console.log("cur_img_bl: " + curr_img_bl)
    setTimeout(rotation_func, time)
}
