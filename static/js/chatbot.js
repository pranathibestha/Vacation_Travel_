const responses = {
  // Existing ones...
  "hi": "Hello! How can I assist you with your travel plans?",
  "hello": "Hi there! Need help with destinations or booking?",
  "how are you": "I'm great! Ready to help you explore amazing places!",

  // New ones
  "what is sanchari": "SANCHARI is a travel planning web app offering curated packages across India.",
  "aim of this project": "The main aim is to simplify travel planning by providing region-wise packages with estimated costs for food, travel, and stay.",
  "features of this project": "It includes login/register, regional travel packages, budget/luxury options, payment estimation, chatbot support, and email confirmation.",
  "how to book a trip": "After logging in, select a region → choose a package → view details → enter number of persons → confirm payment.",
  "is login necessary": "Yes, login is required to access regions and book trips.",
  "how are prices calculated": "Prices are calculated per person by summing food, travel, and stay costs, multiplied by number of persons.",
  "what happens after booking": "You'll receive a confirmation email with full details of your trip.",
  "who can use this app": "Anyone interested in planning travel across Indian regions, whether for tourism or short trips!",
  "can i get travel tips": "Yes! You can ask about destinations, best times to visit, or budget-friendly suggestions.",
  "is there a chatbot": "Yes, TravelBot is available on the homepage to guide and assist you with any questions!"
};

function getBotResponse(input) {
  input = input.toLowerCase().trim();

  if (responses[input]) {
    return responses[input];
  }

  if (input.includes("place") || input.includes("destination")) {
    return "We have amazing destinations! Choose a region to get started.";
  }
  if (input.includes("cost") || input.includes("price") || input.includes("charge")) {
    return "Prices vary by destination. Please pick one to see full details.";
  }
  if (input.includes("book") || input.includes("payment")) {
    return "You can book a trip by selecting a package and proceeding to payment.";
  }

  return "I'm sorry, I didn't understand that. Please ask about destinations, packages, or booking.";
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const chat = document.querySelector(".chat");

  // ✅ DEFAULT MESSAGES when chatbot opens
  appendMessage("Bot", "Hi! I'm TravelBot 🤖");
  appendMessage("Bot", "Ask me anything about destinations, bookings, or packages!");
  appendMessage("Bot", "Example: 'What is SANCHARI?', 'How to book a trip?', or 'Features of this project'");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    appendMessage("You", userMessage);
    const botReply = getBotResponse(userMessage);
    appendMessage("Bot", botReply);

    input.value = "";
  });

  function appendMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
  }

  // 🔁 Toggle chatbot open/close
  document.getElementById("chat-toggle").addEventListener("click", function () {
    const chatBox = document.getElementById("chat-container");
    if (chatBox.style.display === "none" || chatBox.style.display === "") {
      chatBox.style.display = "flex";
      chatBox.style.flexDirection = "column";
    } else {
      chatBox.style.display = "none";
    }
  });
});
