var loadActive = true;

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
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200)
			callback(xmlHttp.responseText);
	}
	var params = 'w={0}&h={1}&x={2}&y={3}&scl={4}'.format(w,h,mid.x,mid.y,scl);
	xmlHttp.open('GET', 'http://95.215.47.224:8000?' + params, true);
	xmlHttp.send(null);
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
	var canvas = document.getElementById("mainView");
	var ds = 16;
	canvas.width = window.innerWidth - ds;
	canvas.height = window.innerHeight - ds;
	var mid = new Point(canvas.width / 2.0, canvas.height / 2.0);
	requestPicture(canvas.width, canvas.height, mid, 1, function(m){
		loadActive = false;
		console.log(m);
	});
	var rad = Math.min(mid.x, mid.y) * 0.1
	var ctx = canvas.getContext('2d');
	console.log(mid.x, mid.y, rad);
	var ang = 0;
	setInterval(function() {
			if(loadActive) {
				var a = ang * Math.PI / 180;
				loadBalls(ctx, mid, rad, a);
				ang = (ang + 3) % 360;
			}
		}, 20);
}
