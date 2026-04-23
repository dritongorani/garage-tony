const chatToggle = document.getElementById("chatToggle");
const chatWidget = document.getElementById("chatWidget");
const chatClose = document.getElementById("chatClose");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");

// Set this to your backend endpoint, not your secret key.
// Example: const AI_API_URL = "http://localhost:8787/api/chat";
const AI_API_URL = "http://localhost:8787/api/chat";

const cannedAnswers = [
  {
    test: /(prix|tarif|cout|co[uû]te)/i,
    answer: "Les tarifs dependent du modele et de la panne. Le plus rapide est de demander un devis gratuit via le bouton Devis en ligne."
  },
  {
    test: /(zone|ville|deplace|intervention|secteur)/i,
    answer: "Nous intervenons surtout sur Lyon, Meximieux et les communes proches dans le Rhone et l'Ain."
  },
  {
    test: /(rdv|rendez|disponib|quand)/i,
    answer: "Les delais varient selon la periode. Contactez-nous par telephone ou WhatsApp pour une reponse rapide."
  },
  {
    test: /(frein|vidange|distribution|diagnostic|obd|batterie)/i,
    answer: "Oui, ce service est propose a domicile. Envoyez la marque, modele et annee du vehicule pour confirmer."
  }
];

function addMessage(content, sender = "bot") {
  const p = document.createElement("p");
  p.className = sender === "bot" ? "bot-msg" : "user-msg";
  p.textContent = content;
  chatMessages.appendChild(p);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function localFallback(question) {
  const match = cannedAnswers.find((item) => item.test.test(question));
  if (match) {
    return match.answer;
  }
  return "Je peux vous aider sur les services, zones d'intervention et devis. Pour une reponse exacte, laissez vos details dans le formulaire.";
}

async function getBotAnswer(question) {
  if (!AI_API_URL) {
    return localFallback(question);
  }

  try {
    const response = await fetch(AI_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question })
    });
    if (!response.ok) {
      return localFallback(question);
    }
    const data = await response.json();
    if (typeof data.reply === "string" && data.reply.trim()) {
      return data.reply;
    }
    return localFallback(question);
  } catch (error) {
    return localFallback(question);
  }
}

chatToggle.addEventListener("click", () => {
  chatWidget.classList.add("open");
});

chatClose.addEventListener("click", () => {
  chatWidget.classList.remove("open");
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = chatInput.value.trim();
  if (!question) {
    return;
  }

  addMessage(question, "user");
  chatInput.value = "";
  addMessage("Je regarde votre question...", "bot");

  const answer = await getBotAnswer(question);
  const loadingMessage = chatMessages.lastElementChild;
  if (loadingMessage && loadingMessage.textContent === "Je regarde votre question...") {
    loadingMessage.remove();
  }
  addMessage(answer, "bot");
});
