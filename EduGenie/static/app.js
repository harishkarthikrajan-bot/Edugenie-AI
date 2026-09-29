const task = document.getElementById('task');
const inputText = document.getElementById('inputText');
const submitBtn = document.getElementById('submitBtn');
const clearBtn = document.getElementById('clearBtn');
const resultCard = document.getElementById('resultCard');
const result = document.getElementById('result');
const resultTitle = document.getElementById('resultTitle');
const resultType = document.getElementById('resultType');

const labels = { qa: 'Answer', explain: 'Explanation', quiz: 'Quiz', summarize: 'Summary', learn: 'Learning Path' };
const endpoints = { qa: '/qa', explain: '/explain', quiz: '/quiz', summarize: '/summarize', learn: '/learn/recommendations' };

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', "'":'&#39;', '"':'&quot;' }[c]));
}

function renderQuiz(questions) {
  return questions.map((q, qi) => `
    <div class="quiz-question" data-question="${qi}" data-answer="${q.correct_answer}">
      <h3>${qi + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map((opt, oi) => `
        <label class="option"><input type="radio" name="q${qi}" value="${oi}"> ${escapeHtml(opt)}</label>
      `).join('')}
      <button class="quiz-check" type="button" onclick="checkQuestion(${qi})">Check answer</button>
      <div class="quiz-feedback" id="feedback-${qi}"></div>
    </div>
  `).join('');
}

window.checkQuestion = function(qi) {
  const block = document.querySelector(`[data-question="${qi}"]`);
  const selected = block.querySelector(`input[name="q${qi}"]:checked`);
  const feedback = document.getElementById(`feedback-${qi}`);
  block.querySelectorAll('.option').forEach((el, index) => {
    el.classList.remove('correct', 'wrong');
    if (index === Number(block.dataset.answer)) el.classList.add('correct');
  });
  if (!selected) { feedback.textContent = 'Choose an option first.'; return; }
  const correct = Number(selected.value) === Number(block.dataset.answer);
  if (!correct) selected.closest('.option').classList.add('wrong');
  feedback.textContent = correct ? 'Correct! 🎉' : 'Not quite. The correct answer is highlighted.';
};

task.addEventListener('change', () => {
  const placeholders = {
    qa: 'Example: Which is the largest ocean?',
    explain: 'Example: Explain the Pythagoras theorem.',
    quiz: 'Paste a topic or educational passage to create 3 MCQs.',
    summarize: 'Paste the educational passage you want summarized.',
    learn: 'Example: SQL for a beginner who wants to reach an advanced level.'
  };
  inputText.placeholder = placeholders[task.value];
});

clearBtn.addEventListener('click', () => {
  inputText.value = '';
  resultCard.classList.add('hidden');
  result.innerHTML = '';
});

submitBtn.addEventListener('click', async () => {
  const text = inputText.value.trim();
  if (!text) { alert('Please enter a topic, question, or passage.'); return; }
  submitBtn.disabled = true;
  submitBtn.textContent = 'Generating…';
  resultCard.classList.remove('hidden');
  resultTitle.textContent = labels[task.value];
  resultType.textContent = task.value.toUpperCase();
  result.textContent = 'Working on your request…';

  try {
    const response = await fetch(endpoints[task.value], {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed.');
    if (task.value === 'qa') result.textContent = data.answer;
    if (task.value === 'explain') result.textContent = data.explanation;
    if (task.value === 'summarize') result.textContent = data.summary;
    if (task.value === 'learn') result.textContent = data.recommendations;
    if (task.value === 'quiz') result.innerHTML = renderQuiz(data.quiz);
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Generate';
  }
});
