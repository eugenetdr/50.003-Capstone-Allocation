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

var i;
var frames = {};
var delta1 = {};
var delta2 = {};
var industry_colors = 
{
  'Logistics':'rgb(255,0,0)',
  'Integrated Systems': 'rgb(0,255,0)',
  'Defense':'rgb(0,0,255)',
  'Architecture':'rgb(255,192,203)',
  'Entrepreneurship':'rgb(255,255,0)',
  'Internet Security':'rgb(148,0,211)'
};

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
    document.getElementById("toolTip"+(element.id)).style.visibility = "hidden";
    //document.getElementById("toolTip"+(element.id)).disabled = true;

    i = element.id;

    frames[i].moved = true;
    
    //.getAttribute("class");
    frames[i].set("left", `${left}px`);
    frames[i].set("top", `${top}px`);
    setTransform(target, i);
    //get real left and top
    console.log((getComputedStyle(document.getElementById(i).nextElementSibling).transform));
    var real_left = (getComputedStyle(document.getElementById(i).nextElementSibling).transform.split(",")[12].slice(1));
    var real_top = (getComputedStyle(document.getElementById(i).nextElementSibling).transform.split(",")[13].slice(1));

    !isPinch && setLabel(clientX, clientY, `X: ${real_left}px<br/>Y: ${real_top}px`);

  }).on("scale", ({ target, delta, clientX, clientY, isPinch}) => {
    i = element.id;
    
    frames[i].resized = true;
    
    delta1[i] =  delta[0];
    delta2[i] = delta[1];
    const scaleX = frames[i].get("transform", "scaleX") * delta[0];
    const scaleY = frames[i].get("transform", "scaleY") * delta[1];
    frames[i].set("transform", "scaleX", scaleX);
    frames[i].scale_x_var = parseFloat(scaleX);
    frames[i].set("transform", "scaleY", scaleY);
    frames[i].scale_y_var = parseFloat(scaleY);
    setTransform(target, i);
    !isPinch && setLabel(clientX, clientY, `S: ${scaleX.toFixed(2)}, ${scaleY.toFixed(2)}`);

  }).on("rotate", ({ target, beforeDelta, clientX, clientY, isPinch}) => {
    i = element.id;
    frames[i].rotated = true;
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
    document.getElementById("toolTip"+(element.id)).style.visibility = null;
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
function hideMoveable(e, i) {
  //change moveable element level property here and save it!
  document.getElementById(i).nextElementSibling.style.visibility = "hidden";
  document.getElementById(i).setAttribute("data-level", "2");
  document.getElementById(i).style.visibility = "hidden";
}

function initialShowDragbox(e, i){
  console.log(i);
  
  console.log('single clicked moveable!');
  document.getElementById(i).nextElementSibling.style.visibility = "visible";
}

function toolTipHideMoveable(e,i){
  //change moveable element level property here and save it!
  document.getElementById(i).nextElementSibling.style.visibility = "hidden";
  e.target.parentElement.setAttribute("data-level", "2");
  e.target.parentElement.style.visibility = "hidden";
}

//loop through all the objects, initialize them
var industry;

for (var i in myData) {
  console.log(i);
    if (myData.hasOwnProperty(i)) {
        //define level, industry, projectName, sLength, sWidth, actualX, actualY, angle 
        var industry = myData[i].industry;
        var level = myData[i].level;
        var projectName = myData[i].projectName;

        var projectNameSplit = projectName.split(" ");
        var projectNameHTML = '<font size = "0.1px">' + projectNameSplit.join('<br/>') + '</font>';
        console.log(projectNameHTML);

        industryHTML = '<font size = "0.1px">' + industry + '</font>';

        var sLength = myData[i].sLength;
        var sWidth = myData[i].sWidth;
        var actualX = myData[i].actualX;
        var actualY = myData[i].actualY;
        var angle = parseFloat(myData[i].angle);

        var init_scaleX = parseFloat(sWidth)/16.4;
        var init_scaleY = parseFloat(sLength)/16.4;

        var moveableElement = document.createElement("div"); 
        moveableElement.classList.add("moveable");

        //unique id for each project: clusteri_teamj = "cluster" + i + "_team" + j
        moveableElement.setAttribute("id", i);
        moveableElement.setAttribute("data-level", 1);
        moveableElement.setAttribute("ondblclick","hideMoveable(event, " + "'" + i + "'" + ");");
        moveableElement.setAttribute("onclick","initialShowDragbox(event, " + "'" + i + "'" + ");");
        moveableElement.setAttribute("text-align", "center");

        //background rectangle to have color
        var backgroundRectangle = document.createElement("div"); 
        backgroundRectangle.style.width = "16px";
        backgroundRectangle.style.height = "16px";
        backgroundRectangle.style.backgroundColor = industry_colors[industry];
        backgroundRectangle.style.border = "1px solid #000";
        //backgroundRectangle.setAttribute("vertical-align","middle");
        //backgroundRectangle.setAttribute("horizontal-align","middle");
        backgroundRectangle.setAttribute("display", "inline-block");

        moveableElement.appendChild(backgroundRectangle);

        var toolTip = document.createElement("span");
        toolTip.setAttribute("class", "tooltiptext tooltip-top::after");
        toolTip.setAttribute("id", "toolTip"+i);
        //toolTip.appendChild(document.createTextNode(industry));
        
        toolTip.innerHTML = projectNameHTML + "<br/>" + industryHTML;
        toolTip.style.fontSize = "2px";
        toolTip.setAttribute("ondblclick","toolTipHideMoveable(event, " + "'" + i + "'" + ");");

        var closeSpan = document.createElement("span");
        closeSpan.setAttribute("class","sr-only");
        closeSpan.setAttribute("id", "closeSpan"+i);
        
        //commented out the innerHTML, because projectname here is messy
        ///closeSpan.innerHTML = projectNameHTML;

        moveableElement.appendChild(closeSpan);
        moveableElement.appendChild(toolTip);
        //moveableElement.style.backgroundColor = "red";

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

        moveable.id = i;
        moveable.top = 1;
        moveable.bottom = -1;
        moveable.left = 1;
        moveable.right = -1;
        moveable.moved = false;
        moveable.rotated = false;
        

        console.log("the elements real left is: ");
        console.log(getComputedStyle(moveableElement.nextElementSibling).transform.split(",")[12].slice(1));

        console.log("the elements real top is: ");
        console.log(getComputedStyle(moveableElement.nextElementSibling).transform.split(",")[13].slice(1));
        
        //set it to 0,0

        var init_left, init_right, init_top, init_bottom;

        init_left = parseFloat((getComputedStyle(moveableElement).left), 10) - parseFloat(getComputedStyle(moveableElement.nextElementSibling).transform.split(",")[12].slice(1));
        init_top = parseFloat((getComputedStyle(moveableElement).top), 10) - parseFloat(getComputedStyle(moveableElement.nextElementSibling).transform.split(",")[13].slice(1));
        
        init_right = -(init_left);
        init_bottom = -(init_top);

        //commented out to not edit position at all
        
        
        
        moveableElement.style.left = init_left + "px";
        moveableElement.style.top = init_top + "px";
        moveableElement.style.right = init_right + "px";
        moveableElement.style.bottom = init_bottom + "px";
        
        var calculated_left = init_left + actualX + (init_scaleX*6);
        var calculated_right = -(calculated_left);

        moveableElement.style.left = (calculated_left) + "px";
        console.log("set the moveable element left to:");
        console.log(getComputedStyle(moveableElement).left);
        moveableElement.style.right = (calculated_right) + "px";

        var calculated_top = init_top + actualY + (init_scaleY*6);
        var calculated_bottom = -(calculated_top);

        moveableElement.style.top = (calculated_top) + "px";
        console.log("set the moveable element top to:");
        console.log(getComputedStyle(moveableElement).top);
        moveableElement.style.bottom = (calculated_bottom) + "px";
        
        
        //end of translate to position

        var angle_rad = angle*(Math.PI / 180);

        frames[i] = new Scene.Frame({
          //translate: [0,0],
          width: "16.4px",
          height: "16.4px",
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

        

        //now rotate

        var element_matrix = "matrix("+Math.cos(angle_rad)+", "+Math.sin(angle_rad)+", "+(-Math.sin(angle_rad))+", "+Math.cos(angle_rad)+", 0, 0)";
        moveableElement.style.transform = element_matrix;
        moveableElement.style.webkitTransform = element_matrix;

        //dont rotate for now
        frames[i].set("transform", "rotate", `${angle}deg`);
        control_box = moveableElement.nextElementSibling;
        control_box.style.visibility = "hidden";

        console.log("SCALE X IS:" + init_scaleX);
        console.log("SCALE Y IS:" + init_scaleY);


        frames[i].set("transform", "scaleX", init_scaleX);
        frames[i].set("transform", "scaleY", init_scaleY);



        frames[i].set("left", getComputedStyle(moveableElement).left);
        console.log("first rotation left set to");
        console.log(frames[i].get("left"));

        frames[i].set("right", getComputedStyle(moveableElement).right);
        console.log("first rotation right set to");
        console.log(frames[i].get("right"));

        frames[i].set("top", getComputedStyle(moveableElement).top);
        console.log("first rotation top set to");
        console.log(frames[i].get("top"));

        frames[i].set("bottom", getComputedStyle(moveableElement).bottom);
        console.log("first rotation bottom set to");
        console.log(frames[i].get("bottom"));

        moveableElement.style.cssText = frames[i].toCSS();

        frames[i].moved = false;
        frames[i].rotated = false;
        frames[i].resized = false;
        

        attachEvents(moveable);

      }
        

}

$(function() { 
  $("#btnSave").click(function() {
    for (var i in myData) {
        if (myData.hasOwnProperty(i)) {
          var id = "placeholder";
          console.log(i);
                id = i;
                moveable_ele = document.getElementById(id);
                control_box = moveable_ele.nextElementSibling;
                control_box.style.visibility = "hidden";
                var st = getComputedStyle(document.getElementById(id));
                var tr = st.getPropertyValue("-webkit-transform") ||
                        st.getPropertyValue("-moz-transform") ||
                        st.getPropertyValue("-ms-transform") ||
                        st.getPropertyValue("-o-transform") ||
                        st.getPropertyValue("transform") ||
                        "fail...";

                console.log(tr);
                var values = tr.split('(')[1];
                    values = values.split(')')[0];
                    values = values.split(',');
                var a = parseFloat(values[0]);
                var b = parseFloat(values[1]);
                var c = parseFloat(values[2]);
                var d = parseFloat(values[3]);
                console.log(a);
                console.log(b);

                var scale = Math.sqrt(a*a + b*b);
                console.log(scale);
                

                // arc sin, convert from radians to degrees, round
                var sin = b/scale;
                var angle = Math.round(Math.asin(sin) * (180/Math.PI));

                var real_left = (getComputedStyle(moveable_ele.nextElementSibling).transform.split(",")[12].slice(1));
                console.log("real left is " + real_left);
                var real_top = (getComputedStyle(moveable_ele.nextElementSibling).transform.split(",")[13].slice(1));
                console.log("real top is " + real_top);

                var scaleX = frames[id].scale_x_var;
                var scaleY = frames[id].scale_y_var;

                console.log("scalex at first is: " + scaleX);
                
                console.log(scaleX);
                console.log("scaley at first is: " + scaleY);
                console.log(scaleY);
                if(isNaN(scaleX)){
                  scaleX = 1;
                }

                if(isNaN(scaleY)){
                  scaleY = 1;
                }

                console.log(scaleX);
                
                console.log(scaleY);
                
                (myData[i])["level"] = parseInt(moveable_ele.getAttribute("data-level"));
                if(frames[id].resized == true){
                (myData[i])["sLength"] = 16*parseFloat(scaleY);
                (myData[i])["sWidth"] = 16*parseFloat(scaleX);
                }
                if(frames[id].rotated == true){
                (myData[i])["angle"] = angle;
                }
                if(frames[id].moved == true){
                (myData[i])["actualX"] = parseFloat(real_left);
                (myData[i])["actualY"] = parseFloat(real_top);
                }   

          }
          
        }
        var jsonOutput = JSON.stringify(myData);
        document.getElementById("mainlabel").setAttribute("data-json", jsonOutput);
        sendAllocationData();
        screenshot();
        console.log(myData);
  });

});