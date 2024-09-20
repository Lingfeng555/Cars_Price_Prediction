
descargar = false

borrarLocalStorage = false

startPoint = 0

fase1URLS = []

fetch(chrome.runtime.getURL('data/urlsClean.json'))
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error al cargar el archivo: ${response.statusText}`);
    }
    console.log("[DEBUG] Archivo JSON encontrado.");
    return response.json();
  })
  .then(data => {
    fase1URLS = data;
  })
  .catch(error => {
    console.error('Error cargando el JSON:', error);
});



if (descargar) {
    descargarDatos();
}

if (borrarLocalStorage) {
    chrome.storage.local.remove('carDataPrimary', () => {
        console.log("[DEBUG] carDataPrimary eliminado del almacenamiento local.");
    });

    // Setear la currentPage en startpoint
    chrome.storage.local.set({ currentPage: startPoint }, () => {
        console.log("[DEBUG] currentPage seteado en StartPoint:", startPoint);
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


let date = ""
let km = ""
let loc = ""
let vehicleType = ""
let cambio = ""
let numPuertas = ""
let plazas = ""
let cv = ""
let cc = ""
let color = ""
let grkm = ""
let combustible = ""
let garantia = ""
let etiqueta = ""

function extraerData() {

    chrome.storage.local.get('currentPage', (result) => {
        let currentPage = result.currentPage || 0;
        console.log("[DEBUG] URL Nº:", currentPage);
    });
    
    console.log("[DEBUG] Extrayendo datos de la página...");

    {/* TITULO */}
    const titleDiv = document.querySelector('.mt-PanelAdInfo-title');
    const title = titleDiv.querySelector('h1').innerText;

    {/* PRECIO */}
    const carDiv = document.querySelector('.mt-CardAdPrice-cashAmount');
    const price = carDiv.querySelector('h3').innerText;

    //--------------------------------------
    {/* TABLA DE DATOS */}
    //--------------------------------------

    const tableData = document.querySelectorAll('.mt-PanelAdDetails-data li');

    //ASUMIMOS QUE EL PRIMER ELEMENTO SIEMPRE ES LA FECHA
    dateInner = tableData[0].querySelector('strong');
    locInner = tableData[2].querySelector('strong');
    vehicleType = tableData[3].querySelector('strong');

    if (dateInner && dateInner.innerText.length == 4){
        date = dateInner.innerText;
        
    }
    if (locInner){
        loc = locInner.innerText;
    }

    if (vehicleType){
        vehicleType = vehicleType.innerText
    }


   



    checkDataType(tableData[1]);
    //checkDataType(tableData[2]);
    //checkDataType(tableData[3]);
    checkDataType(tableData[4]);
    checkDataType(tableData[5]);
    checkDataType(tableData[6]);
    checkDataType(tableData[7]);
    checkDataType(tableData[8]);
    checkDataType(tableData[9]);
    checkDataType(tableData[10]);
    checkDataType(tableData[11]);
    checkDataType(tableData[12]);
    checkDataType(tableData[13]);



    {/* URL FICHA TÉCNICA */}

    const urlDiv = document.querySelector('.mt-PanelEquipment-cta');
    let url = "N/A";
    if (urlDiv){
        url = urlDiv.querySelector('a').href;
    }


    
    saveData(title, price,url);


}

const checkDataType = (data) => {
    if (!data) {
        return;
    }
    const inner = data.querySelector('strong');
    const cleanData = inner ? inner.innerText : 'N/A';
    const combustibles = ['Gasolina', 'Diésel','Diesel', 'Híbrido', 'Eléctrico', 'Híbrido enchufable','Gas licuado (GLP)','Gas natural (CNG)']

    data = data.textContent;

    if (data.includes('gr/km')) {
        console.log("[DEBUG] GR/KM:",cleanData);
        grkm = cleanData;
    }
    else if (data.includes('km')) {
        km = cleanData;
    }
    else if (data.includes('cv')) {
        cv = cleanData;
    } 
    else if (data.includes('cc')) {
        cc = cleanData;
    }
    else if (data.includes('Puertas')) {
        numPuertas = cleanData;
    }
    else if (data.includes('Plazas')) {
        plazas = cleanData;
    }
    else if (data.includes('Cambio')) {
        cambio = cleanData;
    }
    else if (data.includes('Garantía')) {
        garantia = cleanData;
    }
    else if (data.includes('Etiqueta')) {
        etiqueta = cleanData;
    }
    else if (combustibles.includes(cleanData)) {
        combustible = cleanData;
    }
    else {
        //ASUMO QUE ES EL COLOR
        color = cleanData;
        console.log("[DEBUG] No se ha encontrado el tipo de dato.");
    }




};



const saveData = (title, price,url) => {
    chrome.storage.local.get('carDataPrimary', (result) => {
       let carDataArray = result.carDataPrimary || [];

        const newCarData = {
            title,
            price,
            date,
            km,
            loc,
            vehicleType,
            cambio,
            numPuertas,
            cv,
            cc,
            color,
            grkm,
            combustible,
            garantia,
            etiqueta,
            url
        };

        carDataArray.push(newCarData);

        chrome.storage.local.set({ carDataPrimary: carDataArray }, () => {
            console.log("[DEBUG] Datos actualizados y guardados en el almacenamiento local.");
            console.log("[DEBUG] Datos guardados:", carDataArray );
            
           
            setTimeout(goNextPage, 50);
        });

  
    });
};


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
            console.log("[DEBUG] Todos los datos han sido extraídos.");
        }
    });
}

if (!descargar && !borrarLocalStorage) {
    //cuando la página se termine de lodear
    //window.addEventListener('load', extraerData);  
    extraerData();         
}

