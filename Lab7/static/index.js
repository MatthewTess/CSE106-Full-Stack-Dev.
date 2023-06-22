var content = document.querySelector("#content")

//search specific student & their grade
document.querySelector("#searchGrade").onclick = function () {
    var studentName = window.prompt("Enter student name")
    if (studentName != null) {
        fetch('/grades/' + studentName)
            .then(res => res.json())
            .then(data => { content.innerText = JSON.stringify(data) })
            .catch(error => { content.innerText = "Student does not exist" })
    }
}

//list all students & their grades
document.querySelector("#listGrade").onclick = function () {
    fetch('/grades')
        .then(res => res.json())
        .then(data => { content.innerText = "List of student grades:\n" + JSON.stringify(data, null, " ") })

}

//create a student with grade
document.querySelector("#createGrade").onclick = function () {
    var studentName = window.prompt("Enter student name to add")
    if (studentName != null) {
        var studentGrade = window.prompt("Enter student grade")
        fetch('/grades', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                name: studentName,
                grade: studentGrade
            })
        })
            .then(res => res.json())
            .then(data => {
                content.innerText = "Created" + JSON.stringify({
                    name: studentName,
                    grade: studentGrade
                })
            })
            .catch(error => { content.innerText = "Create failed" })
    }
}

//edit grade of specific student
document.querySelector("#editGrade").onclick = function () {
    var studentName = window.prompt("Enter student name to edit")
    if (studentName != null) {
        var studentGrade = window.prompt("Enter new student grade")

        fetch('/grades/' + studentName, {
            method: 'PUT',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                name: studentName,
                grade: studentGrade
            })
        })
            .then(res => res.json())
            .then(data => {
                content.innerText = "Edited" + JSON.stringify({
                    name: studentName,
                    grade: studentGrade
                })
            })
            .catch(error => { content.innerText = "Student does not exist" })
    }
}

//delete grade of specific student
document.querySelector("#deleteGrade").onclick = function () {
    var studentName = window.prompt("Enter student name to delete")
    if (studentName != null) {
        fetch('/grades/' + studentName, {
            method: 'DELETE'
        })
            .then(res => res.json())
            .then(data => {
                content.innerText = "Deleted" + JSON.stringify({
                    name: studentName
                })
            })
            .catch(error => { content.innerText = "Student does not exist" })
    }
}