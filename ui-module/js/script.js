const apiUrl = "http://127.0.0.1:8000/students"; // Replace with your API URL

// Function to fetch and display all students
async function fetchStudents() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Failed to fetch students.");
        const students = await response.json();
        const tableBody = document.getElementById("student-table-body");
        tableBody.innerHTML = "";

        students.forEach(student => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${student.roll_number}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>${student.grade}</td>
                <td>
                    <button onclick="deleteStudent(${student.roll_number})">Delete</button>
                    <button onclick="editStudent(${student.roll_number}, '${student.name}', ${student.age}, ${student.grade})">Edit</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching students:", error);
    }
}

// Function to add or update a student
async function saveStudent(event) {
    event.preventDefault();

    const roll_number = document.getElementById("roll_number").value.trim();
    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value.trim();
    const grade = document.getElementById("grade").value.trim();

    if (!roll_number || !name || !age || !grade) {
        alert("All fields are required.");
        return;
    }

    const student = {
        roll_number: Number(roll_number),
        name,
        age: Number(age),
        grade: Number(grade),
    };

    const method = document.getElementById("roll_number").readOnly ? "PUT" : "POST";
    const url = method === "POST" ? apiUrl : `${apiUrl}/${roll_number}`;

    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(student),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to save student.");
        }

        console.log("Save Response:", await response.json());
        document.getElementById("form").reset();
        document.getElementById("roll_number").readOnly = false; // Reset to POST mode
        fetchStudents(); // Refresh the list
    } catch (error) {
        console.error("Error saving student:", error);
        alert(error.message);
    }
}

// Function to delete a student
async function deleteStudent(roll_number) {
    try {
        const response = await fetch(`${apiUrl}/${roll_number}`, { method: "DELETE" });
        if (!response.ok) throw new Error("Failed to delete student.");
        fetchStudents(); // Refresh list after operation
    } catch (error) {
        console.error("Error deleting student:", error);
        alert(error.message);
    }
}

// Function to populate form for editing
function editStudent(roll_number, name, age, grade) {
    document.getElementById("roll_number").value = roll_number;
    document.getElementById("roll_number").readOnly = true; // Prevent changing roll_number during update
    document.getElementById("name").value = name;
    document.getElementById("age").value = age;
    document.getElementById("grade").value = grade;
}

// Event listener for form submission
document.getElementById("form").addEventListener("submit", saveStudent);

// Fetch students on page load
fetchStudents();
