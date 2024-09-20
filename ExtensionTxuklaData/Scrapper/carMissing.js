



fase1URLS = []

fetch(chrome.runtime.getURL('data/urlsClean.json'))
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error al cargar el archivo: ${response.statusText}`);
    }
    console.log("Archivo JSON encontrado.");
    return response.json();
  })
  .then(data => {
    fase1URLS = data;
  })
  .catch(error => {
    console.error('Error cargando el JSON:', error);
});



function carMissing() {
    if (document.querySelector(".sui-MoleculeNotification--system")){ 
        console.log("[DEBUG] Coche no encontrado , saltando de URL.");  
        goNextPage();
    }
    setTimeout(1000,goNextPage());
    console.log("[DEBUG] TIPO DE PÁGINA NO RECONOCIDA, SALTANDO DE URL.");

}


const goNextPage = () => {
    chrome.storage.local.get('currentPage', (result) => {
        let currentPage = result.currentPage || 0;
        currentPage++;

        if (currentPage < fase1URLS.length) {
            chrome.storage.local.set({ currentPage }, () => {
                //insert <a> tag with the next URL and click it 

                const a = document.createElement('a');
                a.href = fase1URLS[currentPage];
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);


            });
        } 
        else {
            console.log("Todos los datos han sido extraídos.");
        }
    });
}



window.addEventListener('load', carMissing);

