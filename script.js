
const API_URL = "https://principle-aruba-premiere-ballot.trycloudflare.com";

const promptInput = document.getElementById("prompt");
const imageInput = document.getElementById("imageInput");
const analyzeButton = document.getElementById("analyzeButton");
const createVideoButton = document.getElementById("createVideoButton");

const resultBox = document.getElementById("result");
const preview = document.getElementById("preview");
const videoPreview = document.getElementById("videoPreview");
const downloadVideo = document.getElementById("downloadVideo");

let selectedImage = null;

imageInput.addEventListener("change", function () {
    selectedImage = this.files[0];

    if (!selectedImage) {
        preview.hidden = true;
        return;
    }

    if (!selectedImage.type.startsWith("image/")) {
        resultBox.textContent = "اختر صورة صحيحة.";
        selectedImage = null;
        this.value = "";
        preview.hidden = true;
        return;
    }

    preview.src = URL.createObjectURL(selectedImage);
    preview.hidden = false;
});

analyzeButton.addEventListener("click", async function () {
    const prompt = promptInput.value.trim();

    if (!prompt) {
        resultBox.textContent = "اكتب وصف الفيديو أولاً.";
        return;
    }

    analyzeButton.disabled = true;
    resultBox.textContent = "جاري تحليل الوصف...";

    try {
        const response = await fetch(`${API_URL}/api/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "فشل التحليل");
        }

        resultBox.textContent =
            "تم التحليل بنجاح!\n" +
            "المشهد: " + data.scene + "\n" +
            "النموذج: " + data.model;

    } catch (error) {
        resultBox.textContent = "خطأ: " + error.message;
    } finally {
        analyzeButton.disabled = false;
    }
});

createVideoButton.addEventListener("click", async function () {
    const prompt = promptInput.value.trim();

    if (!selectedImage) {
        resultBox.textContent = "من فضلك اختر صورة أولاً.";
        return;
    }

    if (!prompt) {
        resultBox.textContent = "اكتب وصف الحركة أولاً.";
        return;
    }

    createVideoButton.disabled = true;
    videoPreview.hidden = true;
    downloadVideo.hidden = true;
    resultBox.textContent = "جاري إرسال الصورة والوصف...";

    try {
        const formData = new FormData();
        formData.append("image", selectedImage);
        formData.append("prompt", prompt);

        resultBox.textContent = "جاري الاتصال بمحرك Wan2.2...";

        const response = await fetch(`${API_URL}/api/create-video`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || data.error || "فشل إنشاء الفيديو");
        }

        if (!data.success || !data.video_url) {
            throw new Error(data.error || "لم يتم إرجاع فيديو.");
        }

        const videoUrl = new URL(data.video_url, API_URL).href;

        videoPreview.src = videoUrl;
        videoPreview.hidden = false;

        downloadVideo.href = videoUrl;
        downloadVideo.hidden = false;

        resultBox.textContent = "تم إنشاء الفيديو بنجاح!";

    } catch (error) {
        resultBox.textContent = "تعذر إنشاء الفيديو: " + error.message;
    } finally {
        createVideoButton.disabled = false;
    }
});
