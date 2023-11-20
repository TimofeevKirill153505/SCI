class User2 {
    #age;
    names
    constructor(first_name, last_name, age) {
        this.names = { first_name, last_name }
        this.#age = age
    }

    get age() {
        return this.#age
    }

    set age(value) {
        this.#age = value
    }

    static getString() {
        return "It's from extends inheritance"
    }

    getData() {
        return ` Name ${this.names.first_name} ${this.names.last_name}, Age ${this.age}`
    }
}

class Employee2 extends User2 {
    is_admin;
    constructor(first_name, last_name, age, is_admin) {
        super(first_name, last_name, age)
        this.is_admin = is_admin
    }

    getData() {
        return Employee2.getString() + " " + super.getData() + ` Admin: ${this.is_admin ? 'yes' : 'no'}`
    }
}

emp = new Employee2("Tom", "Hills", 37, true)
document.getElementById("extends").textContent = emp.getData()