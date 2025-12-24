const API_BASE = "http://127.0.0.1:8000";

// Upload policy
async function uploadPolicy() {
  const fileInput = document.getElementById("policyFile");
  const status = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    status.innerText = "Please select a policy file.";
    return;
  }

  status.innerText = "Uploading and processing policy...";
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch(`${API_BASE}/upload-policy`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    status.innerText = `Policy uploaded. Chunks indexed: ${data.chunks_indexed}`;
  } catch (err) {
    status.innerText = "Error uploading policy.";
  }
}

// Ask question
async function askQuestion() {
  const query = document.getElementById("queryInput").value;
  const status = document.getElementById("queryStatus");
  const answerBox = document.getElementById("answerBox");
  const sourcesList = document.getElementById("sourcesList");

  if (!query) {
    status.innerText = "Please enter a question.";
    return;
  }

  status.innerText = "Generating answer...";
  answerBox.innerText = "";
  sourcesList.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    const data = await res.json();
    status.innerText = "Answer generated.";

    answerBox.innerText = data.answer;

    data.sources.forEach(chunk => {
      const li = document.createElement("li");
      li.innerText = chunk;
      sourcesList.appendChild(li);
    });

  } catch (err) {
    status.innerText = "Error generating answer.";
  }
}
