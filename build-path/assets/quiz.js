// Shared retrieval-practice quiz widget for the departure-board lessons.
// Usage:
// <div class="quiz" data-answer="dc|d/c|dc pin">
//   <div class="q">Which pin says whether a byte is a command or data?</div>
//   <input type="text" placeholder="type your answer">
//   <button>Check</button>
//   <div class="feedback"></div>
// </div>
(function () {
  function normalize(s) {
    return s.trim().toLowerCase().replace(/\s+/g, " ");
  }

  function wireQuiz(quiz) {
    const accepted = (quiz.dataset.answer || "")
      .split("|")
      .map(normalize)
      .filter(Boolean);
    const input = quiz.querySelector("input[type=text]");
    const button = quiz.querySelector("button");
    const feedback = quiz.querySelector(".feedback");

    function check() {
      const given = normalize(input.value || "");
      const ok = accepted.includes(given);
      feedback.textContent = ok
        ? "Correct."
        : "Not quite — think it through again before revealing.";
      feedback.className = "feedback " + (ok ? "correct" : "incorrect");
    }

    button.addEventListener("click", check);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") check();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".quiz").forEach(wireQuiz);
  });
})();
