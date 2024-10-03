

const descargarDatos = false
const borrarLocalStorage = false

let phase1Data = []
let startPoint = 0

fetch(chrome.runtime.getURL('data/phase1Clean.json'))
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error al cargar el archivo: ${response.statusText}`);
    }
    console.log("Archivo JSON encontrado.");
    return response.json();
  })
  .then(data => {
    phase1Data = data;
  })
  .catch(error => {
    console.error('Error cargando el JSON:', error);
});



if (borrarLocalStorage) {
    chrome.storage.local.remove('fichasData', () => {
        console.log("[DEBUG] fichasData eliminado del almacenamiento local.");
    });

    // Setear la currentPage en startpoint
    chrome.storage.local.set({ currentFicha: startPoint }, () => {
        console.log("[DEBUG] currentFicha seteado en StartPoint:", startPoint);
    });
    
}

function extractData() {

    chrome.storage.local.get('currentFicha', (result) => {
        let currentPage = result.currentFicha || 0;
        console.log("[DEBUG] FICHA Nº:", currentPage);
    });

    console.log("[DEBUG] Extrayendo 7 primararios...");
    // Selecciona todos los elementos de la lista de detalles técnicos
    const listItems = document.querySelectorAll('.mt-ListModelDetails-listItem');

    // Crear un objeto para almacenar las variables
    const carDetails = {};

    // Recorre cada item para extraer el título y el valor
    listItems.forEach(item => {
    const titleElement = item.querySelector('.mt-ListModelDetails-listItemValue');
    const valueElement = item.querySelector('.mt-ListModelDetails-listItemValue--blackBold');

    if (titleElement && valueElement) {
        // Extraer los valores y guardarlos en el objeto carDetails
        const title = titleElement.textContent.trim();
        const value = valueElement.textContent.trim();

        // Asigna el valor al título correspondiente en el objeto carDetails
        carDetails[title] = value;
    }
    });
    // Mostrar los detalles extraídos en la consola
    extractTableData(carDetails);
}


function extractTableData(primCarDetails) {
    const tableRows = document.querySelectorAll('.react-AtomTable-row');

    const carDetails = {};

    // Iterar sobre las filas de la tabla
    tableRows.forEach(row => {
    const key = row.querySelector('td:first-child .mt-ListModelDetails-tableItem')?.innerText.trim();
    const value = row.querySelector('td:last-child .mt-ListModelDetails-tableItem--strong')?.innerText.trim();
    
    if (key && value) {
        carDetails[key] = value;
    }
    });

    //por si acaso alguno de los datos está en la tabla incial pero no en la ficha

    //join both objects
    const carDetailsFinal = {...primCarDetails, ...carDetails};


    // Mostrar los detalles extraídos
    console.log("[DEBUG] ",carDetails);


    chrome.storage.local.get('fichasData', (result) => {
        const fichasArray = result.fichasData || [];

        console.log(fichasArray);

        fichasArray.push(carDetailsFinal);

        chrome.storage.local.set({ fichasData: fichasArray }, () => {
            console.log("[DEBUG] Datos guardados en el localStorage.");
            goNextPage();
        });
        
    
    });


}


const goNextPage = () => {
    chrome.storage.local.get('currentFicha', (result) => {
        let currentFicha = result.currentFicha || 0;
        currentFicha++;

        if (currentFicha < phase1Data.length) {
            chrome.storage.local.set({ currentFicha }, () => {
                //insert <a> tag with the next URL and click it 
                const a = document.createElement('a');
                a.href = phase1Data[currentFicha].url;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
        } 
        else {
            console.log("[DEBUG] Todos los datos han sido extraídos.");
        }
    });
}



if (!descargarDatos && !borrarLocalStorage) {
    window.addEventListener('load', extractData);           
}

