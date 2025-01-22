const BASE_URL = "http://127.0.0.1:5000";

document.getElementById("createTokenForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.target).entries());
    try {
        const response = await fetch(`${BASE_URL}/tokens/create`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        console.log(result);
    } catch (error) {
        console.error("Error:", error.message);
    }
});
