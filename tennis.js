// JavaScript Document
var canvas = $('#canvas').getContext("2d");

var ball = { position: { x: 0, y:0, z:0 }, velocity : { x:0, y:0, z:0 }, spin : { x: 0, y: 0 }, size: { radius: 0.05 } };
var player1 = new Player();
var player2 = new Player();

var net = { height: 0.9, width: 10, depth: 0.01 };

init();

function Player() {
	return { position: { x:0, y:0, z:0 } };
}

function init() {
	ball.position.x = 8;
	ball.position.y = 5;
	ball.position.z = 1.2;

	setInterval(draw, 10);
}

function draw() {
	ball.velocity.x *= 0.9999;
	ball.velocity.y *= 0.9999;
	ball.velocity.z *= 0.9999;
	ball.velocity.z -= 0.1;
	
	if(ball.position.z < 0.05)
	{
		ball.velocity.z *= -1;
		ball.velocity.x += ball.spin.x;
		ball.velocity.y += ball.spin.y;
		ball.velocity.x *= 0.95;
		ball.velocity.y *= 0.95;
	}
	ball.position.x += ball.velocity.x;
	ball.position.y += ball.velocity.y;
	ball.position.z += ball.velocity.z;
	drawBall(ball);
}

function drawBall(ball) {
	circle(ball.position.x*10, ball.position.y * 10 + ball.position.z * 4, 5);
}

function circle(x,y,r) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI*2, true);
  ctx.closePath();
  ctx.fill();
}

function OnKeyPress(key) {
	
}