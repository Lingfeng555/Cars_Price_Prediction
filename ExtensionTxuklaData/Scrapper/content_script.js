// content_script.js

let descargar = true;


function actualizarDescarga() {
    if (descargar) {
        descargarDatos();
    }
}

function descargarDatos() {
    chrome.storage.local.get('enlaces', (result) => {
        const enlacesActualizados = result.enlaces || [];

        const jsonData = JSON.stringify(enlacesActualizados, null, 2);

        const blob = new Blob([jsonData], { type: 'application/json' });

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'enlaces.json'; // Nombre del archivo de descarga
        a.textContent = 'Descargar enlaces';

        document.body.appendChild(a);
        a.click();

        document.body.removeChild(a);
        URL.revokeObjectURL(url); // Liberar el objeto URL
    });
}


actualizarDescarga(true);


function extraerLinks() {
    const div = document.querySelector('.mt-ListAds');
    if (div) {
        const enlaces = div.querySelectorAll('a');
        const hrefs = [];

        enlaces.forEach(enlace => {
            const href = enlace.getAttribute('href');
            if (href) {
                hrefs.push(href);
            }
        });

        console.log("Enlaces encontrados:", hrefs);

        chrome.storage.local.get('enlaces', (result) => {
            const enlacesGuardados = result.enlaces || [];
            const enlacesUnicos = new Set(enlacesGuardados);
            
            hrefs.forEach(href => enlacesUnicos.add(href));
            const enlacesActualizados = Array.from(enlacesUnicos);

            chrome.storage.local.set({ enlaces: enlacesActualizados }, () => {
                console.log("Enlaces actualizados en el almacenamiento local.");
                console.log("Enlaces guardados:", enlacesActualizados);

                // Activar la descarga si se desea
                actualizarDescarga(); // Cambia el booleano según sea necesario
            });
        });
    } else {
        console.log("No se encontró el div con la clase .mt-ListAds.");
    }
}


function pasarDePagina() {
    const paginationElement = document.querySelector('.sui-MoleculePagination');

    if (paginationElement) {
        const listItems = paginationElement.querySelectorAll('li');
        const listItemsArray = Array.from(listItems);
        const nextBtn = listItemsArray[listItemsArray.length - 1];

        if (nextBtn) {
            console.log("Pasando a la siguiente página.");
            const link = nextBtn ? nextBtn.querySelector('a') : null;
            link.click();
            
            
          } else {
            console.log("No se encontró el botón de la siguiente página.");
          }


    } else {
        console.log('No se encontró el elemento con la clase sui-MoleculePagination.');
    }

    
    
}

function scrollDownSimulado() {
    const totalScroll = 1000; // Total de píxeles a desplazar
    const scrollStep = 214;    // Paso del desplazamiento en píxeles
    const scrollDelay = 50;  // Retraso entre cada paso en milisegundos

    let scrolled = 0;

    function scroll() {
        if (scrolled < totalScroll) {
            window.scrollBy(0, scrollStep);
            scrolled += scrollStep;

            setTimeout(scroll, scrollDelay + Math.random() * 200); 
        }
    }

    scroll();
}



setInterval(scrollDownSimulado, 750);



setInterval(extraerLinks, 5200);


let countdown = 5.5;

function goNextPage() {
  if (countdown > 0) {
    console.log(`Siguiente página en ${countdown} segundos`);
    countdown--;
  } else {
    clearInterval(intervalId);
    pasarDePagina();
  }
}

const intervalId = setInterval(goNextPage, 1000);

  