const resumeInput = document.getElementById("resumeInput");
const uploadText = document.getElementById("uploadText");
const analyzeForm = document.getElementById("analyzeForm");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
 
if (resumeInput) {
    resumeInput.addEventListener("change", () => {
        if (resumeInput.files.length > 0) {
            uploadText.textContent = resumeInput.files[0].name;
        } else {
            uploadText.textContent = "Choose PDF Resume";
        }
    });
}
 
if (analyzeForm) {
    analyzeForm.addEventListener("submit", () => {
        submitBtn.disabled = true;
        submitBtn.classList.add("btn-loading");
        btnText.innerHTML = '<span class="spinner"></span>Analyzing Resume...';
    });
}