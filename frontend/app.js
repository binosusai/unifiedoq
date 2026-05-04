const form = document.querySelector("#idea-form");
const input = document.querySelector("#idea-input");
const result = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.textContent = "Running...";
  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ input: input.value }),
    });
    const data = await response.json();
    result.textContent = data.recommendation;
  } catch (error) {
    result.textContent = `POC request failed: ${error}`;
  }
});

const createProjectBtn = document.querySelector("#create-project-btn");
const projectNameInput = document.querySelector("#project-name");
const keyDisplay = document.querySelector("#key-display");
const issuedKey = document.querySelector("#issued-key");
const proxyKeyInput = document.querySelector("#proxy-key");
const providerInput = document.querySelector("#provider-name");
const proxyPayload = document.querySelector("#proxy-payload");
const runProxyBtn = document.querySelector("#run-proxy-btn");
const proxyResult = document.querySelector("#proxy-result");

createProjectBtn.addEventListener("click", async () => {
  const name = projectNameInput.value.trim();
  if (!name) { alert("Enter a project name"); return; }
  try {
    const res = await fetch("/api/projects", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!res.ok) { throw new Error(`${res.status} ${await res.text()}`); }
    const data = await res.json();
    issuedKey.value = data.api_key;
    keyDisplay.removeAttribute("hidden");
  } catch (err) {
    alert(`Failed: ${err}`);
  }
});

runProxyBtn.addEventListener("click", async () => {
  const api_key = proxyKeyInput.value.trim();
  if (!api_key) { alert("Enter an API key"); return; }
  proxyResult.textContent = "Running proxy...";
  try {
    const res = await fetch("/api/proxy/mock", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        api_key,
        provider: providerInput.value.trim() || "openai",
        payload: proxyPayload.value,
      }),
    });
    const data = await res.json();
    proxyResult.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    proxyResult.textContent = `Error: ${err}`;
  }
});
