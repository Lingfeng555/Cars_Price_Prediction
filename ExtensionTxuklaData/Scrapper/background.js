// background.js
console.log("background.js cargado");

// Verifica que chrome.scripting esté disponible
if (chrome.scripting) {
  console.log("chrome.scripting está disponible.");
} else {
  console.error("chrome.scripting no está disponible.");
}

// Ejecutar script en la pestaña cuando se completa la navegación
chrome.webNavigation.onCompleted.addListener(async function(details) {
  console.log("Navigation completed:", details);

  if (details.url.startsWith("https://www.coches.net/segunda-mano/?pg=")) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId: details.tabId },
        files: ['content_script.js']
      });
      console.log("Script inyectado correctamente.");
    } catch (error) {
      console.error("Error al inyectar el script:", error);
    }
  }
  else (details.url.startsWith("https://www.coches.net/*.aspx")) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId: details.tabId },
        files: ['primaryDataScraper.js']
      });
      console.log("Script inyectado correctamente.");
    } catch (error) {
      console.error("Error al inyectar el script:", error);
    }
  }


}, { url: [{ urlMatches: 'https://www.coches.net/*' }] });
