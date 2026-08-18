// Tracking de visitas temporariamente desabilitado.
// Mantemos a estrutura pronta para futura reativação, sem disparar requisições para endpoints de analytics.
const TRACKING_ENABLED = false;

if (TRACKING_ENABLED) {
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

  sendVisit(location.pathname || "/");

  document.querySelectorAll(".cta").forEach((a) => {
    a.addEventListener("click", () => sendVisit(`outbound:${a.href}`));
  });
}
