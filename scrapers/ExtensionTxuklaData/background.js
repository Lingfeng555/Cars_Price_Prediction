chrome.webRequest.onBeforeRequest.addListener(
    function(details) {

      console.log(details.initiator);
      console.log("HOLAOHLAOHLA")
      

      var aBloquear = [
        ".js",
      ];
     
      if (aBloquear.some(script => details.url.endsWith(script)) && details.initiator.startsWith("https://www.coches.net")) {
        return { cancel: true };
      }


      return {cancel: false};
    },
    {urls: ["<all_urls>"]},
    ["blocking"]
  );


  