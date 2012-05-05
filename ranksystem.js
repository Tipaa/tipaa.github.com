// Edmund Smith 2012
// Do not use anywhere. Or talk about. This is unfinished.

var red1 = new Player(10);
var red2 = new Player(10);
var red3 = new Player(10);
var red4 = new Player(10);

var redTeam = new Team([red1,red2,red3,red4],"Red");

var blue1 = new Player(30);
var blue2 = new Player(1);
var blue3 = new Player(10);
var blue4 = new Player(1);

var blueTeam = new Team([blue1, blue2, blue3, blue4],"Blue");

//alert(getExpectedWinner(redTeam,blueTeam).winner.name+" with chance of "+getExpectedWinner(redTeam,blueTeam).chance);

function Player(level) {
	this.level = level;
}

function Team(players,name) {
	this.players = players;
	this.level = getLevelAverage(players);
	this.name = name;
}

function getLevelAverage(players) {
	var level = 0;
	for(var i = 0; i < players.length; i++) {
		level += (players[i].level*1);
	}
	return level / players.length;;
}

function getExpectedWinner(red,blue) {
	return { winner: betterTeam(red, blue), chance: chance(red, blue) };
}
//Gives the statistical chance, then gets as percentage, then multiplies by a -atan(-x) for a nice curve for skill difference blurring
function chance(red, blue) {
	var pct = betterTeam(red, blue).level / (red.level+blue.level) *100;
	var scale = 20;
	var lblur = -Math.atan(-Math.abs(red.level-blue.level)/scale)
	return pct * lblur;
}

function betterTeam(red, blue) {
	return (red.level>blue.level)?red:blue;
}

function worseTeam(red, blue) {
	return (red.level>blue.level)?blue:red;
}