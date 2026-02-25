const API_VISIT = "/api/visit";

async function sendVisit(page) {
  try {
    await fetch(API_VISIT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ page }),
    });
  } catch (e) {
    /* non-blocking */
  }
}

// send page visit on load
sendVisit(location.pathname || "/");

// optional: track outbound case-study clicks
document.querySelectorAll(".cta").forEach((a) => {
  a.addEventListener("click", () => sendVisit(`outbound:${a.href}`));
});

// No parallax JS required: background-attachment:fixed handles the effect.
