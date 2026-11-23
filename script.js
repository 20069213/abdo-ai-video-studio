
const API_URL = "https://YOUR-BACKEND-URL.onrender.com";

const promptInput = document.getElementById("prompt");
const imageInput = document.getElementById("imageInput");
const analyzeButton = document.getElementById("analyzeButton");
const resultBox = document.getElementById("result");
const preview = document.getElementById("preview");

// معاينة الصورة المختارة
imageInput.addEventListener("change", function () {
    const file = this.files[0];

    if (!file) {
        preview.hidden = true;
        return;
    }

    if (!file.type.startsWith("image/")) {
        resultBox.textContent = "من فضلك اختر صورة صحيحة.";
        this.value = "";
        preview.hidden = true;
        return;
    }

    const imageURL = URL.createObjectURL(file);

    preview.src = imageURL;
    preview.hidden = false;
});

// تحليل وصف الفيديو
analyzeButton.addEventListener("click", async function () {
    const prompt = promptInput.value.trim();

    if (!prompt) {
        resultBox.textContent = "اكتب وصف الفيديو أولاً.";
        return;
    }

    analyzeButton.disabled = true;
    resultBox.textContent = "جاري تحليل الوصف...";

    try {
        const response = await fetch(
            `${API_URL}/api/analyze`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ prompt })
            }
        );

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || "Analysis failed");
        }

        resultBox.textContent =
            "تم التحليل بنجاح!\n" +
            "المشهد: " + data.scene + "\n" +
            "النموذج: " + data.model;

    } catch (error) {
        resultBox.textContent =
            "تعذر الاتصال بالسيرفر.\n" +
            "تأكد من تشغيل Backend وإعداد رابط API.\n" +
            error.message;
    } finally {
        analyzeButton.disabled = false;
    }
});
