let cb = document.getElementById("#hide");
function GetData(id) {
  $("#hide").toggle();
  {
    $.get("http://127.0.0.1:8000/" + id, function (data, status) {
      // var text = data.substring(85, 100);
      // console.log(data)
      // var text = data.replace(/<script[^>]*>(?:(?!<\/script>)[^])*<\/script>/g, "");
      const imageElement = new Image();
      imageElement.src = data;
      imageElement.width = 300;
      //document.getElementById('imageContainer').appendChild(imageElement);
      $("#div_" + id).append(imageElement);
    });
  }
}
