// Dark Mode Toggle
document.getElementById('darkModeToggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
});
const dropZone = document.getElementById('dropZone');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.style.backgroundColor = '#e9ecef';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.backgroundColor = '';
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    fileInput.files = event.dataTransfer.files;
    updateFileName(file);
});

// Detect file selection via input
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        updateFileName(fileInput.files[0]);
    }
});

// Update file name display
function updateFileName(file) {
    if (file) {
        fileNameDisplay.textContent = `Uploaded: ${file.name}`;
    }
}

// Upload CSV
function uploadFile() {
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a CSV file to upload.');
        return;
    }

    updateFileName(file); // Ensure filename is displayed

    const reader = new FileReader();

    reader.onload = function (e) {
        try {
            const data = e.target.result;
            const rows = parseCSV(data);
            enhanceData(rows);
            displayData(rows);
        } catch (error) {
            alert('Error processing the file: ' + error.message);
        }
    };

    reader.readAsText(file);
}

// Parse CSV data
function parseCSV(data) {
    const rows = data.split('\n').map(row => row.split(','));
    return rows;
}

// Enhance Data (e.g., Adding Placement chances)
function enhanceData(rows) {
    if (rows.length === 0) return;

    const headers = rows[0];
    rows[0].push('%', 'Generate');

    for (let i = 1; i < rows.length; i++) {
        const percentage = Math.random() * 100;
        rows[i].push(percentage.toFixed(2));
        rows[i].push('<button onclick="generateReport(' + i + ')">Generate</button>');
    }
}

// Display Data in Table
function displayData(rows) {
    const dataSection = document.getElementById('data-section');
    const dataTable = document.getElementById('dataTable');
    dataTable.innerHTML = '';

    const fragment = document.createDocumentFragment();

    rows.forEach((row, rowIndex) => {
        const tr = document.createElement('tr');

        row.forEach(cell => {
            const cellElement = document.createElement(rowIndex === 0 ? 'th' : 'td');
            cellElement.innerHTML = cell.trim();
            tr.appendChild(cellElement);
        });

        fragment.appendChild(tr);
    });

    dataTable.appendChild(fragment);

    dataSection.style.display = 'block';
    updateDashboard(rows);
    document.getElementById('dashboard').style.display = 'block';
}

// Update Dashboard
function updateDashboard(rows) {
    const totalRecords = rows.length - 1;
    const percentages = rows.slice(1).map(row => parseFloat(row[row.length - 2]));
    const averagePercentage = (percentages.reduce((a, b) => a + b, 0) / percentages.length).toFixed(2);

    const placementChance = percentages.filter(percentage => percentage >= 70).length;
    const placementPercentage = ((placementChance / totalRecords) * 100).toFixed(2);

    document.getElementById('totalRecords').textContent = totalRecords;
    document.getElementById('averagePercentage').textContent = `${averagePercentage}%`;

    // Progress bar with percentage label
    const progressBarContainer = document.getElementById('placementChance');
    progressBarContainer.innerHTML = `
        <div class="progress-bar-container">
            <div class="progress-bar" style="width: ${placementPercentage}%;"></div>
        </div>
        <p>${placementPercentage}%</p>
    `;

    renderCharts(percentages);
}

// Render Charts (Bar & Pie Charts)
function renderCharts(data) {
    const ctx = document.getElementById('chart').getContext('2d');

    const ranges = [0, 20, 40, 60, 80, 100];
    const studentCounts = new Array(ranges.length - 1).fill(0);

    data.forEach(percentage => {
        for (let i = 0; i < ranges.length - 1; i++) {
            if (percentage >= ranges[i] && percentage < ranges[i + 1]) {
                studentCounts[i]++;
                break;
            }
        }
    });

    // Bar Chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ranges.slice(0, ranges.length - 1).map((range, index) => `${range}% - ${ranges[index + 1]}%`),
            datasets: [{
                label: 'Number of Students',
                data: studentCounts,
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                borderColor: '#007BFF',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1500
            },
            scales: {
                x: { title: { display: true, text: 'Percentage Range' } },
                y: { title: { display: true, text: 'Number of Students' }, beginAtZero: true }
            }
        }
    });

    // Pie Chart
    // new Chart(pieCtx, {
    //     type: 'pie',
    //     data: {
    //         labels: ranges.slice(0, ranges.length - 1).map((range, index) => `${range}% - ${ranges[index + 1]}%`),
    //         datasets: [{
    //             label: 'Student Distribution',
    //             data: studentCounts,
    //             backgroundColor: ['#FF5733', '#33FF57', '#5733FF', '#33FFF6', '#FFC300'],
    //         }]
    //     }
    // });
}

// Search and Filter
function searchData() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.getElementById('dataTable').rows;

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].cells;
        let match = false;

        for (let j = 0; j < cells.length; j++) {
            if (cells[j].innerText.toLowerCase().includes(searchInput)) {
                match = true;
                break;
            }
        }

        rows[i].style.display = match ? '' : 'none';
    }
}

// Export Data to CSV
function exportToCSV() {
    const rows = document.getElementById('dataTable').rows;
    const csvContent = Array.from(rows)
        .map(row => Array.from(row.cells).map(cell => cell.textContent).join(','))
        .join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'student_data.csv';
    link.click();
}
// Function to generate and download PDF report for a student
function generateReport(index) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Get table data
    const table = document.getElementById("dataTable");
    if (!table || index >= table.rows.length) {
        alert("Invalid student index!");
        return;
    }

    // Adjust column indexes based on your table structure
    const studentID = table.rows[index].cells[0].innerText;
    const studentName = table.rows[index].cells[1].innerText;
    const academicPercentage = table.rows[index].cells[2].innerText;
    const placementChance = table.rows[index].cells[3].innerText;

    // Add content to PDF
    doc.setFont("helvetica", "bold");
    doc.text("Student Placement Report", 20, 20);

    doc.setFont("helvetica", "normal");
    doc.text(`Student ID: ${studentID}`, 20, 40);
    doc.text(`Name: ${studentName}`, 20, 50);
    doc.text(`Academic Percentage: ${academicPercentage}%`, 20, 60);
    doc.text(`Placement Chances: ${placementChance}`, 20, 70);

    // Save the PDF with a dynamic name
    doc.save(`Student_Report_${studentID}.pdf`);
}

// Advanced Filtering by Placement Percentage
function filterByPercentage(min, max) {
    const rows = document.getElementById('dataTable').rows;

    for (let i = 1; i < rows.length; i++) {
        const percentage = parseFloat(rows[i].cells[rows[i].cells.length - 2].innerText);
        rows[i].style.display = (percentage >= min && percentage <= max) ? '' : 'none';
    }
}

// Reset Filters
function resetFilters() {
    const rows = document.getElementById('dataTable').rows;

    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = '';
    }
}

// document.getElementById('addStudentForm').addEventListener('submit', async (e) => {
//     e.preventDefault();  // Prevents page reload

//     const formData = {};
//     const formElements = document.getElementById('addStudentForm').elements;

//     for (let i = 0; i < formElements.length; i++) {
//         const element = formElements[i];
//         if (element.name) {
//             formData[element.name] = element.type === 'number' ? parseFloat(element.value) || null : element.value;
//         }
//     }

//     try {
//         const response = await fetch('http://localhost:5000/add-student', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify(formData)
//         });

//         if (response.ok) {
//             alert('✅ Student details added successfully!');
//             document.getElementById('addStudentForm').reset();
//         } else {
//             const errorData = await response.json();
//             alert('❌ Error: ' + errorData.error);
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('❌ Failed to connect to the server.');
//     }
// });





document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addStudentForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload

        let formData = new FormData(this);
        let jsonData = {};
        formData.forEach((value, key) => { jsonData[key] = value });

        fetch("/add_student", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "Form submitted successfully!");
            this.reset();
        })
        .catch(error => console.error("Error:", error));
    });
});

