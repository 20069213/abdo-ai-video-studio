
const API_URL = "https://principle-aruba-premiere-ballot.trycloudflare.com";

const promptInput = document.getElementById("prompt");
const imageInput = document.getElementById("imageInput");
const analyzeButton = document.getElementById("analyzeButton");
const createVideoButton = document.getElementById("createVideoButton");

const resultBox = document.getElementById("result");
const preview = document.getElementById("preview");
const videoPreview = document.getElementById("videoPreview");
const downloadVideo = document.getElementById("downloadVideo");

const previewPlaceholder = document.querySelector(".preview-placeholder");
const videoPlaceholder = document.querySelector(".video-placeholder");

let selectedImage = null;
let imageObjectUrl = null;

function showMessage(message) {
    resultBox.textContent = message;
}

imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) {
        selectedImage = null;
        preview.hidden = true;
        if (previewPlaceholder) previewPlaceholder.hidden = false;
        return;
    }

    if (!file.type.startsWith("image/")) {
        showMessage("اختر ملف صورة صحيح.");
        this.value = "";
        selectedImage = null;
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showMessage("حجم الصورة أكبر من 10 ميجابايت.");
        this.value = "";
        selectedImage = null;
        return;
    }

    selectedImage = file;

    if (imageObjectUrl) {
        URL.revokeObjectURL(imageObjectUrl);
    }

    imageObjectUrl = URL.createObjectURL(file);

    preview.src = imageObjectUrl;
    preview.hidden = false;

    if (previewPlaceholder) {
        previewPlaceholder.hidden = true;
    }

    showMessage("تم اختيار الصورة بنجاح. اكتب وصف الحركة.");
});

analyzeButton.addEventListener("click", async function () {
    const prompt = promptInput.value.trim();

    if (!prompt) {
        showMessage("اكتب وصف الفيديو أولاً.");
        return;
    }

    analyzeButton.disabled = true;
    showMessage("جاري تحليل الوصف...");

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

        showMessage(
            "تم التحليل بنجاح!\n" +
            "المشهد: " + data.scene + "\n" +
            "النموذج: " + data.model
        );

    } catch (error) {
        showMessage("خطأ في التحليل: " + error.message);
    } finally {
        analyzeButton.disabled = false;
    }
});

createVideoButton.addEventListener("click", async function () {
    const prompt = promptInput.value.trim();

    if (!selectedImage) {
        showMessage("من فضلك اختر صورة أولاً.");
        return;
    }

    if (!prompt) {
        showMessage("اكتب وصف الحركة أولاً.");
        return;
    }

    createVideoButton.disabled = true;
    videoPreview.hidden = true;
    downloadVideo.hidden = true;

    if (videoPlaceholder) {
        videoPlaceholder.hidden = false;
    }

    showMessage("جاري تجهيز الصورة والوصف...");

    try {
        const formData = new FormData();
        formData.append("image", selectedImage);
        formData.append("prompt", prompt);

        showMessage("جاري الاتصال بمحرك Wan2.2...");

        const response = await fetch(`${API_URL}/api/create-video`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || data.error || "فشل إنشاء الفيديو"
            );
        }

        if (!data.success || !data.video_url) {
            throw new Error(data.error || "لم يتم إرجاع فيديو.");
        }

        const videoUrl = new URL(data.video_url, API_URL).href;

        videoPreview.src = videoUrl;
        videoPreview.hidden = false;

        if (videoPlaceholder) {
            videoPlaceholder.hidden = true;
        }

        downloadVideo.href = videoUrl;
        downloadVideo.hidden = false;

        showMessage("تم إنشاء الفيديو بنجاح! اضغط تشغيل لمشاهدته.");

    } catch (error) {
        showMessage("تعذر إنشاء الفيديو: " + error.message);
    } finally {
        createVideoButton.disabled = false;
    }
});

window.addEventListener("beforeunload", function () {
    if (imageObjectUrl) {
        URL.revokeObjectURL(imageObjectUrl);
    }
});
