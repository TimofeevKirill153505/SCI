class MyDate {
    year;
    month;
    day;

    constructor(year, month, day) {
        this.year = year
        this.month = month
        this.day = day
    }

    static fromString(string) {
        let reg = /(\d\d\d\d)-(\d{1,2})-(\d{1,2})/
        let res = string.match(reg)
        //console.log(string)
        return new MyDate(parseInt(res[1]), parseInt(res[2]), parseInt(res[3]))
    }

    toString() {
        return `${this.year}-${this.month}-${this.day}`
    }

    static readFromLocalStorage() {
        let ls = localStorage.getItem("dates")
        let reg = /([\d\-]*)/
        let res = ls.match(reg)
        let dates = []
        for (let date of res) {
            //console.log(date)
            dates.push(MyDate.fromString(date))
        }
        let string = ""

        for (let date of spring_dates) {
            string += date.toString() + ', '
        }
        if (string) string = string.slice(0, -2)
        console.log(string)

        return dates
    }
}

function dtk(date) {
}
dates = [new MyDate(2023, 11, 20), new MyDate(2023, 4, 17), new MyDate(2023, 11, 20), new MyDate(2023, 11, 20),
new MyDate(2020, 5, 15), new MyDate(2023, 1, 9)]
set = new Set()
for (date of dates) {
    set.add(date)
}

spring_dates = []
for (date of set) {
    if (date.month >= 3 && date.month <= 5) spring_dates.push(date)
}
string = ""
for (date of spring_dates) {
    string += date.toString() + ', '
}
if (string) string = string.slice(0, -2)
// console.log(string)
localStorage.setItem("dates", string)

dates = MyDate.readFromLocalStorage()


string = ""
for (date of spring_dates) {
    string += `year: ${date.year}, month: ${date.month}, day: ${date.day}` + "\n"
}

document.getElementById("dates").textContent = string
