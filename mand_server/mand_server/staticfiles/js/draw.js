"use strict";

var address = 'vitchenko.xyz:80';
var loadActive = true;
var image = null;
var bg = null;
var screenSize;
var mouseDownIn;
var picShift;
var context;
var scl = 3;
var samplesCount = 100;
var mathpos;
var preset=0;
var inputSamp;
var inputZoom;
var inputX;
var inputY;

function sclXY() {
	if(screenSize.x > screenSize.y) {
		return new Point((screenSize.x / screenSize.y) * scl, scl)
	} else {
		return new Point(scl, (screenSize.y / screenSize.x) * scl)
	}
}

if (!String.prototype.format) {
  String.prototype.format = function() {
      var args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) { 
        return typeof args[number] != 'undefined'
		        ? args[number]
		        : match
		      ;
	    });
    };
}

function Point(x,y) {
	this.x = x;
	this.y = y;
	this.add = function(pt) {
		return new Point(this.x + pt.x, this.y + pt.y);
	}
	this.mul = function(c) {
		return new Point(this.x * c, this.y * c);
	}
	this.len = function() {
		return Math.sqrt((this.x * this.x) + (this.y * this.y));
	}
	this.normal = function() {
		var l = this.len();
		return new Point(this.x / l, this.y / l);
	}
}

function requestPicture(w, h, mid, scl, callback) {
	loadActive = true;
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			//var blob = new Blob([xmlHttp.response], {type: 'image/png'});
			//var url = URL.createObjectURL(blob);
			//callback(url);
			var js = JSON.parse(xmlHttp.responseText);
			callback(js['target'], js['bg'])
		}
	}
	var params = 'a=reg&w={0}&h={1}&x={2}&y={3}&scl={4}&samp={5}&clr={6}'.format(w,h,mid.x,mid.y,scl,samplesCount,preset);
	xmlHttp.open('GET', 'http://' + address + '/render?' + params, true);
	xmlHttp.responseType = "text";
	xmlHttp.send(null);
}

function openHighRes() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
			var js = JSON.parse(xmlHttp.responseText);
			var w = window.open(js['target'], '_blank');
			if(w)
				w.focus();
			else
				alert("can't open window :(");
		}
	}
	var w = screenSize.x;
	var h = screenSize.y;
	var mid = mathpos;
	var params = 'a=hi&w={0}&h={1}&x={2}&y={3}&scl={4}&samp={5}&clr={6}'.format(w * 2,h * 2,mid.x,mid.y,scl,samplesCount,preset);
	xmlHttp.open('GET', 'http://' + address + '/render?' + params, true);
	xmlHttp.responseType = "text";
	xmlHttp.send(null);
}

var waitfor = 0;
function drawImg(urlt,urlb) {
	console.log(urlt, urlb)
	image = new Image();
	bg = new Image();
	var t = new Date().getTime();
	image.src = urlt + '/?' + t;
	bg.src = urlb + '/?' + t;
	waitfor = 2;
	function loaded() {
		waitfor -= 1;
		loadActive = false;
		if(waitfor == 0) {
			context.drawImage(image, 0, 0, screenSize.x, screenSize.y)
		}
	}
	image.onload = loaded;
	bg.onload = loaded;
}

function redrawPic() {
	var bgp = screenSize.mul(-1).add(picShift);
	context.drawImage(bg, bgp.x, bgp.y, screenSize.x * 3, screenSize.y * 3);
	context.drawImage(image, picShift.x, picShift.y, screenSize.x, screenSize.y);
}

function mouseMove(e) {
	var now = new Point(e.screenX, e.screenY);
	picShift = now.add(mouseDownIn.mul(-1));
	redrawPic();
}

function newView() {
	var s = sclXY();
	var x = mathpos.x - (picShift.x / screenSize.x) * s.x;
	var y = mathpos.y - (picShift.y / screenSize.y) * s.y;
	//console.log(mathpos.x, mathpos.y, x, y);
	mathpos.x = x;
	mathpos.y = y;
	inputSamp.value = samplesCount;
	inputZoom.value = scl;
	inputX.value = mathpos.x;
	inputY.value = mathpos.y;
	requestPicture(screenSize.x, screenSize.y, mathpos, scl, drawImg);
	picShift.x = 0;
	picShift.y = 0;
}

function pint (a) {var i = parseInt(a); if(isNaN(i)) {throw 'NaN';} else {return i;}};
function pfloat (a) {var i = parseFloat(a); if(isNaN(i)) {throw 'NaN';} else {return i;}};

/*
function fromInputs() {
	try {
		samplesCount = pint(inputSamp.value);
	inputZoom.value = scl;
	inputX.value = mathpos.x;
	inputY.value = mathpos.y;
}*/

function zoom(c) {
	scl = scl * c;
	newView();
	//requestPicture(screenSize.x, screenSize.y, mathpos, scl, drawImg);
}

function loadBalls(ctx,mid,rad,ang) {
	ctx.fillStyle = 'white';
	ctx.strokeStyle = 'black';
	ctx.lineWidth = 5;
	
	ctx.beginPath();
	var r = rad * 3 + ctx.lineWidth;
	ctx.rect(mid.x - r, mid.y - r, r * 2, r * 2);
	ctx.fill();
	ctx.closePath();
	
	ctx.beginPath();
	var center = mid.add(new Point(Math.cos(ang), Math.sin(ang)).mul(rad * 2));
	ctx.arc(center.x, center.y, rad, 0, 2*Math.PI, false);
	ctx.fill();
	ctx.stroke();

	ctx.beginPath();
	var center = mid.add(new Point(Math.cos(ang), Math.sin(ang)).mul(-rad * 2));
	ctx.arc(center.x, center.y, rad, 0, 2*Math.PI, false);
	ctx.fill();
	ctx.stroke();
}

window.onload = function() {
	document.documentElement.style.overflow = 'hidden'; // scrollbar off
	var canvas = document.getElementById("mainView");
	inputSamp = document.getElementById("samples");
	inputSamp.onchange = function() {
		try {
			samplesCount = pint(inputSamp.value);
			newView();
		} catch(a) {}
	}
	inputZoom = document.getElementById("zoom");
	inputZoom.onchange = function() {
		try {
			scl = pfloat(inputZoom.value);
			newView();
		} catch(a){}
	}
	inputX = document.getElementById("x");
	inputX.onchange = function() {
		try {
			mathpos.x = pfloat(inputX.value);
			newView();
		} catch(a){}
	}
	inputY = document.getElementById("y");
	inputY.onchange = function() {
		try {
			mathpos.y = pfloat(inputY.value);
			newView();
		} catch(a){}
	}
	var ds = 16;
	canvas.width = document.body.clientWidth;//window.innerWidth - ds;
	canvas.height = document.body.clientHeight;//window.innerHeight - ds;
	var btndown = false;
	canvas.onmousedown = function(e) {
		if(!loadActive) {
			picShift = new Point(0, 0);
			mouseDownIn = new Point(e.screenX, e.screenY);
			btndown = true;
		}
	}
	canvas.onmouseup = function() {
		if(btndown) {
			btndown = false;
			newView();
		}
	}
	canvas.onmousemove = function(e) {
		if(btndown) {
			mouseMove(e)
		}
	}
	var pres = [90,88,67,86,66,78];
	document.onkeydown = function(e) {
		console.log(e.keyCode);
		if(e.keyCode == 187) { // +
			zoom(0.5);
		} else if(e.keyCode == 189) { // -
			zoom(2);
		} else if(e.keyCode == 70) {
			openHighRes()
		} else {
			for(var i=0; i<pres.length; ++i)
				if(pres[i] == e.keyCode) {
					preset = i;
					newView();
					return;
				}
		}
	}
	screenSize = new Point(canvas.width, canvas.height);
	mathpos = new Point(0,0);
	picShift = new Point(0,0);
	var ctx = canvas.getContext('2d');
	context = ctx;
	newView();
	/*
	requestPicture(canvas.width, canvas.height, mid, 3, function(a,b){
		//loadActive = false;
		drawImg(ctx, a,b);
	});
	*/

	/*
	var rad = Math.min(mid.x, mid.y) * 0.1
	console.log(mid.x, mid.y, rad);
	var ang = 0;
	setInterval(function() {
			if(loadActive) {
				var a = ang * Math.PI / 180;
				loadBalls(ctx, mid, rad, a);
				ang = (ang + 3) % 360;
			}
		}, 20);
	*/
}