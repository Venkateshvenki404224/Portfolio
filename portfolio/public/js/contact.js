document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contact-form");
  const messagesDiv = form.querySelector(".messages");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Clear messages
      messagesDiv.innerHTML = "";

      // Get values
      const name = form.querySelector("[name='name']").value.trim();
      const email = form.querySelector("[name='email']").value.trim();
      const subject = form.querySelector("[name='subject']").value.trim();
      const message = form.querySelector("[name='message']").value.trim();

      // Optionally: client-side checks, for better UX (backend also validates)
      if (!name || !email || !subject || !message) {
        messagesDiv.innerHTML = `<div class="text-red-500 mb-2">All fields are required.</div>`;
        return;
      }

      // Disable form submit button to avoid duplicate submits
      const btn = form.querySelector("button[type='submit']");
      btn.disabled = true;
      btn.classList.add("opacity-60");

      function getCsrfToken() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
      }

      fetch("/api/method/portfolio.portfolio.api.submit_contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-Frappe-CSRF-Token": getCsrfToken()
        },
        body: new URLSearchParams({
          name, email, subject, message
        })
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === "success") {
            messagesDiv.innerHTML = `<div class="text-green-500 mb-2">${data.message}</div>`;
            form.reset();
          } else {
            messagesDiv.innerHTML = `<div class="text-red-500 mb-2">${data.message || "Error sending message"}</div>`;
          }
        })
        .catch(() => {
          messagesDiv.innerHTML = `<div class="text-red-500 mb-2">An error occurred. Please try again.</div>`;
        })
        .finally(() => {
          btn.disabled = false;
          btn.classList.remove("opacity-60");
        });
    });
  }
});
