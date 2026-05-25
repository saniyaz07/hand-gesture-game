// Simulate GTA loading transitions
const highlights = [
  "Machine Learning 95/100",
  "Mission Passed: RoadX OCR",
  "Lives Safeguarded: Digital Partograph",
  "Premium AI Ops | Eclipse Towers"
];

let i = 0;
setInterval(() => {
  document.querySelector('.loading-screen').textContent = highlights[i];
  i = (i + 1) % highlights.length;
}, 3000);
