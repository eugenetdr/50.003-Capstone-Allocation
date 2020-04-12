var container = document.getElementsByClassName("container")[0];

var allocation = document.currentScript.getAttribute('one');

var foo = ((allocation).replace(/&(l|g|quo)t;/g, function(a,b){
  return {
      l   : '<',
      g   : '>',
      quo : '"'
  }[b];
}));

  foo = foo.replace(/u'/g, '\'')
  foo = foo.replace(/'/g, '\"')

  console.log(foo);

  var myData = JSON.parse(foo);
  console.log("parsed json data for allocation is: ");
  console.log(myData);

  //steps: i. loop through each cluster
  // ii. get the center points of the cluster and rotation angle
  // iii. Then loop through each of the projects, use formula to find final position of each project
  //then use final position and rotation angle to intialize them 

var i;
var frames = {};

function firstRotateTransform(target, i){
  frames[i].set("left", getComputedStyle(target).left);
  console.log("first rotation left set to");
  console.log(frames[i].get("left"));

  frames[i].set("right", getComputedStyle(target).right);
  console.log("first rotation right set to");
  console.log(frames[i].get("right"));

  frames[i].set("top", getComputedStyle(target).top);
  console.log("first rotation top set to");
  console.log(frames[i].get("top"));

  frames[i].set("bottom", getComputedStyle(target).bottom);
  console.log("first rotation bottom set to");
  console.log(frames[i].get("bottom"));

  target.style.cssText = frames[i].toCSS();
}

function setTransform(target, i) {
  target.style.cssText = frames[i].toCSS();
  }

const labelElement = document.querySelector(".label");

function setLabel(clientX, clientY, text) {
  labelElement.style.cssText = `display: block; transform: translate(${clientX}px, ${clientY - 10}px) translate(-100%, -100%);`;
  labelElement.innerHTML = text;
  }


//define the event handler attaching functions
function attachEvents(element){
  element.on("pinch", ({ clientX, clientY}) => {
    i = element.id;
    setTimeout(() => {
      setLabel(clientX, clientY, `X: ${frames[i].get("left")}
  <br/>Y: ${frames[i].get("top")}
  <br/>W: ${frames[i].get("width")}
  <br/>H: ${frames[i].get("height")}
  <br/>S: ${frames[i].get("transform", "scaleX").toFixed(2)}, ${frames[i].get("transform", "scaleY").toFixed(2)}
  <br/>R: ${parseFloat(frames[i].get("transform", "rotate")).toFixed(1)}deg
  `);
    });
  }).on("drag", ({ target, left, top, clientX, clientY, isPinch}) => {

    i = element.id;
    
    //.getAttribute("class");
    frames[i].set("left", `${left}px`);
    frames[i].set("top", `${top}px`);
    setTransform(target, i);
    //get real left and top
    var real_left = (getComputedStyle(document.getElementById(i).nextElementSibling).transform.split(",")[12].slice(1));
    var real_top = (getComputedStyle(document.getElementById(i).nextElementSibling).transform.split(",")[13].slice(1));
    console.log("style of the control box is");
    console.log(getComputedStyle(document.getElementById(i).nextElementSibling));
    //document.getElementsByClassName("sr-only")[0];
    !isPinch && setLabel(clientX, clientY, `X: ${real_left}px<br/>Y: ${real_top}px`);

  }).on("scale", ({ target, delta, clientX, clientY, isPinch}) => {
    i = element.id;
    const scaleX = frames[i].get("transform", "scaleX") * delta[0];
    const scaleY = frames[i].get("transform", "scaleY") * delta[1];
    frames[i].set("transform", "scaleX", scaleX);
    frames[i].set("transform", "scaleY", scaleY);
    setTransform(target, i);
    !isPinch && setLabel(clientX, clientY, `S: ${scaleX.toFixed(2)}, ${scaleY.toFixed(2)}`);

  }).on("rotate", ({ target, beforeDelta, clientX, clientY, isPinch}) => {
    i = element.id;
    const deg = parseFloat(frames[i].get("transform", "rotate")) + beforeDelta;

    frames[i].set("transform", "rotate", `${deg}deg`);
    if(element.rotated == false){
      console.log("first rotation!");
      firstRotateTransform(target, i);
      element.rotated = true;
    }
    else{
      setTransform(target, i);
    }
    //console.log("transform of the element is");
    //console.log(getComputedStyle(document.getElementById("moveable_"+i)).transform);

    console.log("transform of the control box is");
    console.log(getComputedStyle(document.getElementById(i).nextElementSibling.firstChild).transform);
    !isPinch && setLabel(clientX, clientY, `R: ${deg.toFixed(1)}`);
  }).on("resize", ({ target, width, height, clientX, clientY, isPinch}) => {
    i = element.id;
    frames[i].set("width", `${width}px`);
    frames[i].set("height", `${height}px`);
    setTransform(target, i);
    !isPinch &&  setLabel(clientX, clientY, `W: ${width}px<br/>H: ${height}px`);
  }).on("warp", ({ target, multiply, delta, clientX, clientY}) => {
    i = element.id;
    frames[i].set("transform", "matrix3d", multiply(frames[i].get("transform", "matrix3d"), delta));
    setTransform(target, i);

    setLabel(clientX, clientY, `X: ${clientX}px<br/>Y: ${clientY}px`);
  }).on("dragEnd", () => {
    labelElement.style.display = "none";
  }).on("scaleEnd", () => {
    labelElement.style.display = "none";
  }).on("rotateEnd", () => {
    labelElement.style.display = "none";
  }).on("resizeEnd", () => {
    labelElement.style.display = "none";
  }).on("warpEnd", () => {
    labelElement.style.display = "none";
  });

  window.addEventListener("resize", () => {
      element.updateRect();
  });

}

//function to make box invisible upon double click
function hideMoveable(e) {
  //change moveable element level property here and save it!

  e.target.nextSibling.style.visibility = "hidden";
  e.target.setAttribute("data-level", "1");
  e.target.style.visibility = "hidden";
  // e.target -> element that was clicked
}

function toolTipHideMoveable(e){
  //change moveable element level property here and save it!
  e.target.parentElement.nextSibling.style.visibility = "hidden";
  e.target.parentElement.setAttribute("data-level", "1");
  e.target.parentElement.style.visibility = "hidden";
}

//loop through all the objects, initialize them
var industry;

for (var i in myData) {
  console.log(i);
    if (myData.hasOwnProperty(i)) {
        //define Cx, Cy, Angle, ClusLength, ClusWidth, then C
        var Cx = myData[i].clusPos.x;
        var Cy = myData[i].clusPos.y;
        var Angle = myData[i].clusAngle;
        var ClusLength = myData[i].clusLength;
        var ClusWidth = myData[i].clusBreadth;
        var offset_x = Cx - (ClusWidth/2);
        var offset_y = Cy + (ClusLength/2);


        for(var j in (myData[i])["teams"]){
          console.log(j);
          if(((myData[i])["teams"]).hasOwnProperty(j)){
            //get relx, rely, industry
            var relX = myData[i].teams[j].relativeX;
            var relY = myData[i].teams[j].relativeY;
            var projectName = myData[i].teams[j].projectName;

            industry = myData[i].teams[j].industry;

            var moveableElement = document.createElement("div"); 
            moveableElement.classList.add("moveable");

            //unique id for each project: clusteri_teamj = "cluster" + i + "_team" + j
            moveableElement.setAttribute("id", i + "_" + j);
            moveableElement.setAttribute("ondblclick","hideMoveable(event);");

            var toolTip = document.createElement("span");
            toolTip.setAttribute("class", "tooltiptext tooltip-top::after");
            toolTip.appendChild(document.createTextNode(industry));
            toolTip.style.fontSize = "20px";
            toolTip.setAttribute("ondblclick","toolTipHideMoveable(event);");

            var closeSpan = document.createElement("span");
            closeSpan.setAttribute("class","sr-only");
            
            closeSpan.appendChild(document.createTextNode("Move!"));

            moveableElement.appendChild(closeSpan);
            moveableElement.appendChild(toolTip);

            container.appendChild(moveableElement);
            
            var moveable = new Moveable(moveableElement.parentElement, {
              target: moveableElement,
              origin: false,
              draggable: true,
              rotatable: true,
              scalable: true,
              pinchable: true,
              keepRatio: false,
              throttleDrag: 1,
              throttleScale: 0.01,
              throttleRotate: 0.2,
              throttleResize: 1,
            })

            moveable.id = i + "_" + j;
            moveable.top = 1;
            moveable.bottom = -1;
            moveable.left = 1;
            moveable.right = -1;
            moveable.moved = false;
            moveable.rotated = false;

            frames[i + "_" + j] = new Scene.Frame({
              translate: [0,0],
              width: myData[i].teams[j].sWidth + "px",
              height: myData[i].teams[j].sLength + "px",
              left: "0px",
              top: "0px",
              transform: {
                rotate: "0deg",
                scaleX: 1,
                scaleY: 1,
                matrix3d: [
                  1, 0, 0, 0,
                  0, 1, 0, 0,
                  0, 0, 1, 0,
                  0, 0, 0, 1,
                ],
              },
            });

            attachEvents(moveable);

            //This section changes the x and y to the objective
            //formula: Rx = Cx + (Ox  * cos(θ)) - (Oy * sin(θ)), ox = width/2, Cy = center about which you are rotating
            //         Ry = Cy + (Ox  * sin(θ)) + (Oy * cos(θ))
            //rotating point ()
            
            //vars involved: Cx, Cy, relX, relY, offset_x, offset_y
            var angle_rad = Angle*(Math.PI / 180);
            console.log("Cx from dict is " + Cx);
            console.log("Cy from dict is " + Cy);
            console.log("relX from dict is " + relX);
            console.log("relY from dict is " + relY);
            console.log("offset_x from dict is " + offset_x);
            console.log("offet_y from dict is " + offset_y);
            console.log("angle in radians from dict is " + angle_rad);
            //var objective_left = Cx + (relX + offset_x - Cx)*Math.cos(angle_rad) - ((-relY) + offset_y - Cy)*Math.sin(angle_rad); //calculate this using the formula
            //var objective_top = Cy + ((-relY) + offset_y - Cy)*Math.cos(angle_rad) + (relX + offset_x - Cx)*Math.sin(angle_rad); //calculate this using the formula

            var objective_left = Cx + (relX - Cx)*Math.cos(angle_rad) - ((relY) - Cy)*Math.sin(angle_rad); //calculate this using the formula
            var objective_top = Cy + ((relY) - Cy)*Math.cos(angle_rad) + (relX - Cx)*Math.sin(angle_rad); //calculate this using the formula



            console.log("calculated new left is " + objective_left);
            console.log("calculated new top is " + objective_top);
            //to make left of ele = objective_left - actual_left
            //make top of ele = objective top + actual_top

            var previous_transform = getComputedStyle(document.getElementById(i + "_" + j).nextElementSibling).transform.split(",");

            console.log("previous 3d matrix(actual left, actual top) was:");
            console.log(previous_transform);

            actual_left = parseFloat(previous_transform[12]);
            console.log("actual left of previous position was: " + actual_left);
            actual_top = parseFloat(previous_transform[13]);
            console.log("actual top of previous position was: " + actual_top);

            var calculated_left = (objective_left - actual_left + offset_x);
            var calculated_right = -(objective_left - actual_left + offset_x);

            //hardcoded

            //calculated_left = 400;
            //calculated_right = -400;

            //adjustments because of default (870,0)

            moveableElement.style.left = (calculated_left) + "px";
            console.log("set the moveable element left to:");
            console.log(getComputedStyle(moveableElement).left);
            moveableElement.style.right = (calculated_right) + "px";

            var calculated_top = (objective_top + offset_y);
            var calculated_bottom = (-(objective_top + offset_y));
            //hardcoded

            //calculated_top = 400;
            //calculated_bottom = -400;

            //adjustments, because we have to convert the bottom left point to top left point

            moveableElement.style.top = (calculated_top) + "px";
            console.log("set the moveable element top to:");
            console.log(getComputedStyle(moveableElement).top);
            moveableElement.style.bottom = (calculated_bottom) + "px";

            //set the 12th and 13th elements of 3d matrix to objective left and top
            //use string.replace and parseFloat
            
            previous_transform[12] = (calculated_left+858).toString();
            previous_transform[13] = calculated_top.toString();
            previous_transform = previous_transform.join(",");
            moveableElement.nextElementSibling.style.transform = previous_transform;
            moveableElement.style = moveableElement.nextElementSibling.style;
            
            //end of x,y translation
            
            //Now, rotate angle
            
            
            
            var element_matrix = "matrix("+Math.cos(angle_rad)+", "+Math.sin(angle_rad)+", "+(-Math.sin(angle_rad))+", "+Math.cos(angle_rad)+", 0, 0)";
            moveableElement.style.transform = element_matrix;
            moveableElement.style.webkitTransform = element_matrix;

            frames[i + "_" + j].set("transform", "rotate", `${Angle}deg`);

            frames[i + "_" + j].set("left", getComputedStyle(moveableElement).left);
            console.log("first rotation left set to");
            console.log(frames[i + "_" + j].get("left"));

            frames[i + "_" + j].set("right", getComputedStyle(moveableElement).right);
            console.log("first rotation right set to");
            console.log(frames[i + "_" + j].get("right"));

            frames[i + "_" + j].set("top", getComputedStyle(moveableElement).top);
            console.log("first rotation top set to");
            console.log(frames[i + "_" + j].get("top"));

            frames[i + "_" + j].set("bottom", getComputedStyle(moveableElement).bottom);
            console.log("first rotation bottom set to");
            console.log(frames[i + "_" + j].get("bottom"));

            moveableElement.style.cssText = frames[i + "_" + j].toCSS();
            

          }
        }
    }
}

$(function() { 
  $("#btnSave2").click(function() { 
    html2canvas($("#pageMain")[0]).then(function(canvas) {
      theCanvas = canvas;
              canvas.toBlob(function(blob) {
                  saveAs(blob, "Dashboard_2.png"); 
              });
      });
  });
});

  //n cluster i
/*
  var Cx = myData[i].clusPos.x;
  var Cy = myData[i].clusPos.y;
  var Angle = myData[i].clusAngle;
  var ClusLength = myData[i].clusLength;
  var ClusWidth = myData[i].clusWidth;
  var offset_x = Cx - (ClusWidth/2);
  var offset_y = Cy - (ClusLength/2);

  for(j=0; j<myData[i].teams.length; j++){

    var relX = myData[i].teams[j].relativeX;
    var relY = myData[i].teams[j].relativeY;

    industry = myData[i].teams[j].industry;

    var moveableElement = document.createElement("div"); 
    moveableElement.classList.add("moveable");

    //unique id for each project: clusteri_teamj = "cluster" + i + "_team" + j
    moveableElement.setAttribute("id", i + "_" + j);
    moveableElement.setAttribute("ondblclick","hideMoveable(event);");

    var toolTip = document.createElement("span");
    toolTip.setAttribute("class", "tooltiptext tooltip-top::after");
    toolTip.appendChild(document.createTextNode(industry));
    toolTip.style.fontSize = "20px";
    toolTip.setAttribute("ondblclick","toolTipHideMoveable(event);");

    var closeSpan = document.createElement("span");
    closeSpan.setAttribute("class","sr-only");
    
    closeSpan.appendChild(document.createTextNode("Move!"));

    moveableElement.appendChild(closeSpan);
    moveableElement.appendChild(toolTip);

    container.appendChild(moveableElement);
    
    var moveable = new Moveable(moveableElement.parentElement, {
      top: 1, left: 1, right: -1, bottom: -1,
      target: moveableElement,
      origin: false,
      draggable: true,
      rotatable: true,
      scalable: true,
      pinchable: true,
      keepRatio: false,
      throttleDrag: 1,
      throttleScale: 0.01,
      throttleRotate: 0.2,
      throttleResize: 1,
    })

    moveable.id = i + "_" + j;
    moveable.top = 1;
    moveable.bottom = -1;
    moveable.left = 1;
    moveable.right = -1;
    moveable.moved = false;
    moveable.rotated = false;

    frames[i + "_" + j] = new Scene.Frame({
      translate: [0,0],
      width: myData[i].teams[j].width + "px",
      height: myData[i].teams[j].height + "px",
      left: "0px",
      top: "0px",
      transform: {
        rotate: "0deg",
        scaleX: 1,
        scaleY: 1,
        matrix3d: [
          1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1, 0,
          0, 0, 0, 1,
        ],
      },
    });

    attachEvents(moveable);

    //This section changes the x and y to the objective
    //formula: Rx = Cx + (Ox  * cos(θ)) - (Oy * sin(θ)), ox = width/2, Cy = center about which you are rotating
    //         Ry = Cy + (Ox  * sin(θ)) + (Oy * cos(θ))
    //rotating point ()
    var angle_rad = Angle*(Math.PI / 180);
    objective_left = Cx + (relX + offset_x - Cx)*Math.cos(angle_rad) - (relY + offset_y - Cy)*Math.sin(angle_rad); //calculate this using the formula
    objective_top = Cy + (relY + offset_y - Cy)*Math.cos(angle_rad) + (relX + offset_x - Cx)*Math.sin(angle_rad); //calculate this using the formula
    //to make left of ele = objective_left - actual_left
    //make top of ele = objective top + actual_top

    var previous_transform = getComputedStyle(document.getElementById(i + "_" + j).nextElementSibling).transform.split(",");

    console.log("previous 3d matrix(actual left, actual top) was:");
    console.log(previous_transform);

    actual_left = parseFloat(previous_transform[12]);
    actual_top = parseFloat(previous_transform[13]);

    moveableElement.style.left = (objective_left - actual_left) + "px"
    console.log("set the moveable element left to:");
    console.log(moveableElement.style.left);
    moveableElement.style.right = (-(objective_left - actual_left)) + "px";

    moveableElement.style.top = (objective_top + actual_top) + "px"
    console.log("set the moveable element top to:");
    console.log(moveableElement.style.top);
    moveableElement.style.bottom = (-(objective_top + actual_top)) + "px";

    //set the 12th and 13th elements of 3d matrix to objective left and top
    //use string.replace and parseFloat
    
    previous_transform[12] = objective_left.toString();
    previous_transform[13] = objective_top.toString();
    moveableElement.nextElementSibling.style.transform = previous_transform;
    //end of x,y translation
    
    //Now, rotate angle
    
    
    var element_matrix = "matrix("+Math.cos(angle_rad)+", "+Math.sin(angle_rad)+", "+(-Math.sin(angle_rad))+", "+Math.cos(angle_rad)+", 0, 0)";
    moveableElement.style.transform = element_matrix;
    moveableElement.style.webkitTransform = element_matrix;

    frames[i + "_" + j].set("transform", "rotate", `${Angle}deg`);

    frames[i + "_" + j].set("left", getComputedStyle(moveableElement).left);
    console.log("first rotation left set to");
    console.log(frames[i + "_" + j].get("left"));

    frames[i + "_" + j].set("right", getComputedStyle(moveableElement).right);
    console.log("first rotation right set to");
    console.log(frames[i + "_" + j].get("right"));

    frames[i + "_" + j].set("top", getComputedStyle(moveableElement).top);
    console.log("first rotation top set to");
    console.log(frames[i + "_" + j].get("top"));

    frames[i + "_" + j].set("bottom", getComputedStyle(moveableElement).bottom);
    console.log("first rotation bottom set to");
    console.log(frames[i + "_" + j].get("bottom"));

    moveableElement.style.cssText = frames[i + "_" + j].toCSS();
  }
}
*/