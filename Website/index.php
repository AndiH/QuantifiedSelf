<?php
date_default_timezone_set('Europe/Berlin');
$yesterday = strtotime("yesterday");
$readableYesterday = date("d. M. Y", $yesterday);

require_once('config.inc.php');

require_once('computerinput.inc.php');

class MyDB extends SQLite3
{
	function __construct()
	{
		$this->open('data/fbData.db');
	}
}

$db = new MyDB();
if(!$db){
	echo $db->lastErrorMsg();
} else {
		// echo "Opened database successfully\n";
}

/* the following 7 lines still need to be merged into the code following after that. it's redundant at the moment. */ 
$ret = $db->query("SELECT * from fitbitdata where date = " . $yesterday );
$lastSteps = $lastFloors = "No";
while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
	$lastDate = $row['date'];
	$lastSteps =  $row['steps'];
	$lastFloors = $row['floors'];
}

$today = strtotime('today');
$dates = array();
$queryString = "SELECT * from fitbitdata where ";
$nOfHistoryDays = 10;
for ($i = 1; $i < $nOfHistoryDays; $i++) {
	$currentDate = strtotime('-' . $i . ' day', $today);
	array_push($dates, $currentDate);
	$queryString .= "(date = " . $currentDate . ") ";
	if ($i < ($nOfHistoryDays - 1 )) $queryString .= "OR ";
}

$historySteps = $historyFloors = array();
$historyQuery = $db->query($queryString);
while ($row = $historyQuery->fetchArray()) {
	$historySteps[$row['date']] = $row['steps'];
	$historyFloors[$row['date']] = $row['floors'];
}

function convDate($d) {
	return date("d.m", $d);
}
$jsonHistoryDates = json_encode(array_map("convDate", array_keys($historyFloors)));
$jsonHistorySteps = json_encode(array_values($historySteps));
$jsonHistoryFloors = json_encode(array_values($historyFloors));

$db->close();


/* Stuff for coloring the numbers */
function getColor($value, $limitvalue, $color)
{
	if ($value < ($limitvalue / 3)) return $color["lowlow"];
	if ($value < ($limitvalue * 0.99)) return $color["low"];
	if (($value >= ($limitvalue * 0.99)) && ($value < ($limitvalue * 1.8))) return $color["good"];
	if (($value >= ($limitvalue * 1.8)) && ($value < ($limitvalue * 2.4))) return $color["verygood"];
	if (($value >= ($limitvalue * 2.4)) && ($value < ($limitvalue * 3.8))) return $color["veryverygood"];
	if ($value >= ($limitvalue * 3.8)) return $color["overthetop"];
}
function getGlow($value, $limitvalue)
{
	if ($value >= ($limitvalue * 4)) return true;
}

$colors = array(
	lowlow => "rgb(196, 54, 42)",
	low => "rgb(196, 122, 42)",
	good => "rgb(43, 105, 23)",
	verygood => "rgb(34, 138, 42)",
	veryverygood => "rgb(12, 159, 206)",
	overthetop => "rgb(0, 92, 255)",
);

$goalSteps = 7000;
$goalFloors = 12;

$colorSteps = getColor($lastSteps, $goalSteps, $colors);
$colorFloors = getColor($lastFloors, $goalFloors, $colors);

if (getGlow($lastSteps, $goalSteps)) $glowSteps = "text-shadow: 0px 0px 20px;";
if (getGlow($lastFloors, $goalFloors)) $glowFloors = "text-shadow: 0px 0px 20px;";
?>

<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<title></title>
	<meta name="description" content="">
	<meta name="viewport" content="width=device-width">

	<link rel="stylesheet" href="css/normalize.min.css">
	<link rel="stylesheet" href="css/main.css">

	<script src="js/vendor/modernizr-2.6.2.min.js"></script>
	<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css">

	<link href='http://fonts.googleapis.com/css?family=Average+Sans|Ubuntu' rel='stylesheet' type='text/css'>
	<link href='font/font.css' rel='stylesheet' type='text/css'>
	<link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
	<style type="text/css">
		html {
			font-family: "Ubuntu";
		}
		#header, #content {
			margin: auto;
			text-align: center;
			padding: 20px;
			width: 600px;
		}
		#content {
			height: 200px;
		}
		#header {
			margin-top: 10px;
			bottom: inherit;
		}
		span.number, h1 {
			font-family: 'Average Sans', sans-serif;
		}
		span.number {
			font-size: 3em;
		}
		h1 {
			color: #7A7A7A;
			opacity: 0.8;
		}
		h1:hover {
			opacity: 1;
		}
		div.steps {
			<?php if ($colorSteps) echo "color: " . $colorSteps . ";"; ?>
			<?php if ($glowSteps) echo $glowSteps; ?>
		}
		div.stairs {
			<?php if ($colorFloors) echo "color: " . $colorFloors . ";"; ?>
			<?php if ($glowFloors) echo $glowFloors; ?>
		}
		div.keypresses, div.clicks {
			color: #3C5079;
		}
		.number:before {
			font-family: "andiliveregular";
			position: relative;
			font-size: 0.7em;
			padding-right: 10px;
			opacity: 0.6;
			line-height: 1;
			font-weight: normal;
			font-style: normal;
			-webkit-font-smoothing: antialiased;
			-moz-osx-font-smoothing: grayscale;
		}
		.number:hover:before {
			opacity: 0.8;
		}
		.icon-footprints:before {
			content: "s";
		}
		.icon-stairs:before {
			content: "a";
		}
		.icon-clicks:before {
			content: "p";
			padding-right: 4px;
		}
		.number.icon-keypresses:before {
			font-family: FontAwesome;
			content: "\f11c";
			bottom: 3px;
		}
		.chart {
			margin-top: 100px;
		}
		h1 {
			cursor: pointer;
		}
		#header h1 {
			cursor: default;
		}
		h1 i {
			font-size: 0.6em;
			position: relative;
			bottom: 4px;
			padding-right: 4px;
		}
		canvas#graph {
/* 			overflow: hidden; */
			display: none;
			margin-bottom: 10px;
		}
		div.about {
			padding-bottom: 10px;
		}
		div.text-about {
			display: none;
		}
		
	</style>
</head>
<body>
<!--[if lt IE 7]>
	<p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
	<![endif]-->
	<div id="header">
		<div class="date">
			<h1><?php echo $readableYesterday ?></h1>
		</div>
	</div>
	<div id="content">
		<div class="steps">
			<span class="number icon-footprints" title="<?php echo $lastSteps ?> steps walked yesterday."><?php echo $lastSteps ?></span>
		</div>
		<div class="stairs">
			<span class="number icon-stairs" title="<?php echo $lastFloors ?> floors climbed yesterday."><?php echo $lastFloors ?></span>
		</div>
		<div class="keypresses">
			<span class="number icon-keypresses" title="<?php echo $lastKeys ?> keys pressed yesterday."><?php echo $lastKeys ?></span>
		</div>
		<div class="clicks">
			<span class="number icon-clicks" title="<?php echo $lastClicks ?> clicked with my mouse yesterday."><?php echo $lastClicks ?></span>
		</div>
		<div class="chart">
			<h1 id="history"><i class="fa fa-toggle-down"></i>History</h1>
			 <canvas id="graph" height="250" width="600"></canvas>
		</div>
		<div class="about">
			<h1><i class="fa fa-toggle-down"></i>About</h1>
			<div class="text-about">
				<p>The steps I walk daily are tracked by my Fitbit. This website displays the amount of steps I walked yesterday – if available, otherwise it will just print <em>No</em>. Also, there's a graph showing the distribution of walked steps of the last nine days.<br/>
				This project is part of my <a href="http://www.andisblog.de/?s=quantified+self">Quantified Self studies</a>.
				</p>
				<p>The code to this project (including Fitbit-Api→SQLite-DB in Python as well as the PHP code running what you currently see) is <a href="https://github.com/AndiH/QuantifiedSelf/tree/master/Fitbit">available at Github</a>.</p>
			</div>
	</div>

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
	<script>window.jQuery || document.write('<script src="js/vendor/jquery-1.10.1.min.js"><\/script>')</script>
	<script src="//code.jquery.com/ui/1.10.3/jquery-ui.js"></script>

	<script src="js/plugins.js"></script>
	<script src="js/main.js"></script>
	<script src="js/Chart.js"></script>
	<script>
		var chartData = {
	 	labels : <?php echo $jsonHistoryDates ?>,
		 	datasets : [{
			 	fillColor : "rgba(220,220,220,0.5)",
		        strokeColor : "rgba(220,220,220,1)",
		        pointColor : "rgba(220,220,220,1)",
		        pointStrokeColor : "#fff",
		        data : <?php echo $jsonHistoryFloors ?>
		 	},
			{
				fillColor : "rgba(151,187,205,0.5)",
				strokeColor : "rgba(151,187,205,1)",
				pointColor : "rgba(151,187,205,1)",
				pointStrokeColor : "#fff",
				data : <?php echo $jsonHistorySteps ?>
			}]
		}
/* 		var myLine = new Chart(document.getElementById("graph").getContext("2d")).Line(chartData); */
		
		var firstRun = true;
		$(".chart #history").click(function() {
			if (firstRun) {
				var myLine = new Chart($("#graph").get(0).getContext("2d")).Line(chartData);
				firstRun = false;
			} 
			$("canvas").toggle("blind");
			$('html, body').animate({ 
					scrollTop: $(document).height()
				}, 
				1400, 
				"easeOutQuint"
			);
			$(".chart i").toggleClass("fa-toggle-up fa-toggle-down");
		});
		$(".about h1").click(function() {
			$(".text-about").toggle("blind");
			$('html, body').animate({
					scrollTop: $(document).height()
				},
				1400,
				"easeOutQuint"
			);
			$(".about i").toggleClass("fa-toggle-up fa-toggle-down");
		})
	</script>
	
</body>
</html>
