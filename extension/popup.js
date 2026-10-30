document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultBox = document.getElementById('resultBox');
  const scoreBadge = document.getElementById('scoreBadge');
  const tierDesc = document.getElementById('tierDesc');
  const tipsList = document.getElementById('tipsList');
  const titleInput = document.getElementById('titleInput');

  // Auto-detect title from active YouTube Studio tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0] && tabs[0].id) {
      chrome.tabs.sendMessage(tabs[0].id, { action: "GET_YOUTUBE_TITLE" }, (response) => {
        if (response && response.title) {
          titleInput.value = response.title;
        }
      });
    }
  });

  analyzeBtn.addEventListener('click', async () => {
    const title = titleInput.value.trim();
    if (!title) {
      alert("Please enter a video title to evaluate.");
      return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerText = "Analyzing...";

    const payload = {
      title: title,
      duration_minutes: parseFloat(document.getElementById('duration').value) || 10,
      tags_count: parseInt(document.getElementById('tagsCount').value) || 10,
      publish_hour: parseInt(document.getElementById('hour').value) || 18,
      publish_dayofweek: parseInt(document.getElementById('day').value) || 4
    };

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error("API service returned an error status");
      const data = await res.json();

      resultBox.style.display = "block";
      scoreBadge.innerText = `${data.score_percentage}% Potential`;

      if (data.score_percentage >= 60) {
        scoreBadge.className = "score-badge high";
        tierDesc.innerText = "🚀 High Performer profile. Strong virality markers.";
      } else if (data.score_percentage >= 40) {
        scoreBadge.className = "score-badge moderate";
        tierDesc.innerText = "⚡ Moderate potential. Room for title improvements.";
      } else {
        scoreBadge.className = "score-badge low";
        tierDesc.innerText = "⏳ Standard initial reach. Follow suggestions below.";
      }

      tipsList.innerHTML = "";
      if (!data.suggestions || data.suggestions.length === 0) {
        const li = document.createElement('li');
        li.innerText = "Metadata and linguistic hooks are well-optimized!";
        tipsList.appendChild(li);
      } else {
        data.suggestions.forEach(tip => {
          const li = document.createElement('li');
          li.innerText = tip;
          tipsList.appendChild(li);
        });
      }
    } catch (err) {
      alert("Could not connect to http://localhost:8000. Please ensure the backend server is running.");
    } finally {
      analyzeBtn.disabled = false;
      analyzeBtn.innerText = "Predict Potential";
    }
  });
});
