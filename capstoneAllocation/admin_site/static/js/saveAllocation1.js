$(function() { 
    $("#btnSaveImage").click(function() { 
      html2canvas($("#pageMain")[0]).then(function(canvas) {
        theCanvas = canvas;
                canvas.toBlob(function(blob) {
                    saveAs(blob, "Dashboard.png");
                });
        });
    });
  });