
descargar = false

borrarLocalStorage = false

fase1URLS = []

fetch(chrome.runtime.getURL('data/enlaces1070.json'))
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


if (descargar) {
    descargarDatos();
}

if (borrarLocalStorage) {
    chrome.storage.local.remove('carDataPrimary', () => {
        console.log("carDataPrimary eliminado del almacenamiento local.");
    });

    // Eliminar la clave currentPage
    chrome.storage.local.remove('currentPage', () => {
        console.log("currentPage eliminado del almacenamiento local.");
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


date = ""
km = ""
location = ""
vehicleType = ""
cambio = ""
numPuertas = ""
plazas = ""
potencia = ""
cv = ""
cc = ""
color = ""
grkm = ""
combustible = ""
garantia = ""
etiqueta = ""

function extraerData() {

    console.log("Extrayendo datos de la página...");

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

    {/* FECHA */}

    const dateData = tableData[0].querySelector('strong');
    const data1 = dateData ? dateData.innerText : 'N/A';

    {/* KILOMETROS */}

    const kmData = tableData[1].querySelector('strong');
    const data2 = kmData ? kmData.innerText : 'N/A';

    checkDataType(data2);

    {/* LOCALIDAD */}

    const locationData = tableData[2].querySelector('strong');
    const data3 = locationData ? locationData.innerText : 'N/A';


    {/* vehicleType */}

    const vehicleTypeData = tableData[3].querySelector('strong');
    const data4 = vehicleTypeData ? vehicleTypeData.innerText : 'N/A';


    {/* CAMBIO */}

    const cambioData = tableData[4].querySelector('strong');
    const data5 = cambioData ? cambioData.innerText : 'N/A';



    {/* NUM PUERTAS */}

    const numPuertasData = tableData[5].querySelector('strong');
    const data6 = numPuertasData ? numPuertasData.innerText : 'N/A';


    {/* PLAZAS */}

    const plazasData = tableData[4].querySelector('strong');
    const data7 = plazasData ? plazasData.innerText : 'N/A';

    //EL RESTO PUEDE QUE NO ESTE



    {/* POTENCIA cc */}

    const potenciaData = tableData[7].querySelector('strong');
    const data8 = potenciaData ? potenciaData.innerText : 'N/A';

    {/*POTENCIA cv */}

    const cvData = tableData[8].querySelector('strong');
    const data9 = cvData ? cvData.innerText : 'N/A';

    {/* COLOR */}

    const colorData = tableData[9].querySelector('strong');
    const data10 = colorData ? colorData.innerText : 'N/A';

    {/* gr/km */}

    const grkmData = tableData[10].querySelector('strong');
    const data11 = grkmData ? grkmData.innerText : 'N/A';

    {/* COMBUSTIBLE */}

    const combustibleData = tableData[11].querySelector('strong');
    const data12 = combustibleData ? combustibleData.innerText : 'N/A';

    {/* Garantía */}

    const garantiaData = tableData[12].querySelector('strong');
    const data13 = garantiaData ? garantiaData.innerText : 'N/A';

    {/* EtiquetaType  */}

    const etiquetaData = tableData[13].querySelector('strong');
    const data14 = etiquetaData ? etiquetaData.innerText : 'N/A';
    

    {/* URL FICHA TÉCNICA */}
    const urlDiv = document.querySelector('.mt-PanelEquipment-cta');
    const data15 = urlDiv.querySelector('a').href;


    
    saveData(title, price,url);


}

const checkDataType = (data) => {
    if (data === 'N/A') {
        return null;
    }
    else if (data.includes('km')) {
        console.log("KM: ", data);
        km = data;
    }
    else if (data.includes('cv')) {
        cv = data;
    } 
    else if (data.includes('cc')) {
        cc = data;
    }
    else if (data.includes('gr/km')) {
        grkm = data;
    }
    else {
        return data;
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


const goNextPage = () => {
    chrome.storage.local.get('currentPage', (result) => {
        let currentPage = result.currentPage || 0;
        currentPage++;

        if (currentPage < fase1URLS.length) {
            chrome.storage.local.set({ currentPage }, () => {
                console.log("Página actualizada:", currentPage);
                
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


//cuando la página se termine de lodear
window.addEventListener('load', extraerData);
