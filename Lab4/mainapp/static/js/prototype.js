function User(first_name, last_name, age) {

    this.names = { first_name, last_name }
    let _age = age
    this.setAge = (age) => { if (age >= 18) return; alert("МЕНЬШЕ 18!!!"); age = undefined }
    this.getAge = () => { return _age }
    this.getData = () => {
        return ` Name ${this.names.first_name} ${this.names.last_name}, Age ${this.getAge()}`
    }
}

User.prototype.getString = function () { return `It's from prototype inheritance`; };
User.prototype.prop = 667

function Employee(first_name, last_name, age, is_admin) {
    User.call(this, first_name, last_name, age)
    this.getData = () => {
        return this.getString() + ` Name ${this.names.first_name} ${this.names.last_name}, Age ${this.getAge()}` +
            ` Admin: ${is_admin ? 'yes' : 'no'}`
    }
    this.is_admin = is_admin
}

Employee.prototype = Object.create(User.prototype)
Employee.prototype.constructor = Employee

emp = new Employee("Tom", "Hills", 37, true)
document.getElementById("prototype").textContent = emp.getData()