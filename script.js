
const imageInput = document.getElementById("image");
const imagePreview = document.getElementById("imagePreview");
const statusBox = document.getElementById("status");

let selectedImage = null;

imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) {
        selectedImage = null;
        imagePreview.style.display = "none";
        return;
    }

    if (!file.type.startsWith("image/")) {
        alert("اختار صورة صحيحة!");
        this.value = "";
        return;
    }

    selectedImage = file;

    const reader = new FileReader();

    reader.onload = function (event) {
        imagePreview.src = event.target.result;
        imagePreview.style.display = "block";
    };

    reader.readAsDataURL(file);
});

function generateTextVideo() {
    const prompt = document.getElementById("prompt").value.trim();

    if (!prompt) {
        alert("اكتب وصف الفيديو الأول!");
        return;
    }

    statusBox.textContent =
        "تم تسجيل فكرة الفيديو: " + prompt;

    alert("تم تسجيل وصف الفيديو بنجاح!");
}

function generateImageVideo() {
    if (!selectedImage) {
        alert("اختار صورة الأول!");
        return;
    }

    const prompt =
        document.getElementById("imagePrompt").value.trim();

    statusBox.textContent =
        "الصورة جاهزة: " + selectedImage.name +
        (prompt ? " | وصف الحركة: " + prompt : "");

    alert("تم تجهيز الصورة للمرحلة القادمة!");
}
