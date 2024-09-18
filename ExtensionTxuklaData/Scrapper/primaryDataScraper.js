
descargar = false

borrarLocalStorage = false

fetch(chrome.runtime.getURL('data/enlaces1070.json'))
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error al cargar el archivo: ${response.statusText}`);
    }
    console.log("Archivo JSON encontrado.");
    return response.json();
  })
  .then(data => {
    console.log("Datos cargados correctamente:");
    console.log(data);
  })
  .catch(error => {
    console.error('Error cargando el JSON:', error);
});



if (descargar) {
    descargarDatos();
}

if (borrarLocalStorage) {
    chrome.storage.local.remove('carDataPrimary', () => {
        console.log("carDataPrimary eliminado del almacenamiento local.");
    });
}

function descargarDatos() {
    chrome.storage.local.get('carDataPrimary', (result) => {
        const carDataArray = result.carDataPrimary || [];

        const jsonData = JSON.stringify(carDataArray, null, 2);

        const blob = new Blob([jsonData], { type: 'application/json' });

        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');

        a.href
            = url;
        a.download = 'carDataPrimary.json'; // Nombre del archivo de descarga
        a.textContent = 'Descargar datos';

        document.body.appendChild(a);
        a.click();

        document.body.removeChild(a);
        URL.revokeObjectURL(url); // Liberar el objeto URL
    });
}



function extraerData() {

    console.log("Extrayendo datos de la página...");

    {/* TITULO */}

    const titleDiv = document.querySelector('.mt-PanelAdInfo-title');
    const title = titleDiv.querySelector('h1').innerText;

    {/* PRECIO */}
    const carDiv = document.querySelector('.mt-CardAdPrice-cashAmount');
    const price = carDiv.querySelector('h3').innerText;

    {/* TABLA DE DATOS */}

    const tableData = document.querySelectorAll('.mt-PanelAdDetails-data li');

    {/* FECHA */}

    const dateData = tableData[0].querySelector('strong');
    const date = dateData ? dateData.innerText : 'N/A';

    {/* KILOMETROS */}

    const kmData = tableData[1].querySelector('strong');
    const km = kmData ? kmData.innerText : 'N/A';

    {/* LOCALIDAD */}

    const locationData = tableData[2].querySelector('strong');
    const location = locationData ? locationData.innerText : 'N/A';


    {/* vehicleType */}

    const vehicleTypeData = tableData[3].querySelector('strong');
    const vehicleType = vehicleTypeData ? vehicleTypeData.innerText : 'N/A';


    {/* CAMBIO */}

    const cambioData = tableData[4].querySelector('strong');
    const cambio = cambioData ? cambioData.innerText : 'N/A';

    {/* PLAZAS */}

    const plazasData = tableData[5].querySelector('strong');
    const plazas = plazasData ? plazasData.innerText : 'N/A';

    {/* NUM PUERTAS */}

    const numPuertasData = tableData[6].querySelector('strong');
    const numPuertas = numPuertasData ? numPuertasData.innerText : 'N/A';

    {/* POTENCIA cc */}

    const potenciaData = tableData[7].querySelector('strong');
    const potencia = potenciaData ? potenciaData.innerText : 'N/A';

    {/*POTENCIA cv */}

    const cvData = tableData[8].querySelector('strong');
    const cv = cvData ? cvData.innerText : 'N/A';

    {/* COLOR */}

    const colorData = tableData[9].querySelector('strong');
    const color = colorData ? colorData.innerText : 'N/A';

    {/* gr/km */}

    const grkmData = tableData[10].querySelector('strong');
    const grkm = grkmData ? grkmData.innerText : 'N/A';

    {/* COMBUSTIBLE */}

    const combustibleData = tableData[11].querySelector('strong');
    const combustible = combustibleData ? combustibleData.innerText : 'N/A';

    {/* Garantía */}

    const garantiaData = tableData[12].querySelector('strong');
    const garantia = garantiaData ? garantiaData.innerText : 'N/A';

    {/* EtiquetaType  */}

    const etiquetaData = tableData[13].querySelector('strong');
    const etiqueta = etiquetaData ? etiquetaData.innerText : 'N/A';
    

    {/* URL FICHA TÉCNICA */}
    const urlDiv = document.querySelector('.mt-PanelEquipment-cta');
    const url = urlDiv.querySelector('a').href;


    
    saveData(title, price, date, km, location, vehicleType, cambio, numPuertas, potencia, cv, color, grkm, combustible, garantia, etiqueta,url);


}


const saveData = (title, price, date, km, location, vehicleType, cambio, numPuertas, potencia, cv, color, grkm, combustible, garantia, etiqueta,url) => {
    chrome.storage.local.get('carDataPrimary', (result) => {
       let carDataArray = result.carDataPrimary || [];

        const newCarData = {
            title,
            price,
            date,
            km,
            location,
            vehicleType,
            cambio,
            numPuertas,
            potencia,
            cv,
            color,
            grkm,
            combustible,
            garantia,
            etiqueta,
            url
        };

        carDataArray.push(newCarData);

        chrome.storage.local.set({ carDataPrimary: carDataArray }, () => {
            console.log("Datos actualizados y guardados en el almacenamiento local.");
            console.log("Datos guardados:", carDataArray );
        });
    });
};


//cuando la página se termine de lodear
window.addEventListener('load', extraerData);
