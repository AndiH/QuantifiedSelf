<?php
date_default_timezone_set('Europe/Berlin');
$yesterday = strtotime("yesterday");
$readableYesterday = date("d. M. Y", $yesterday);

require_once('inc.config.php');
require_once('inc.mysqlconnect.php');

require_once('inc.computerinput.php');
require_once('inc.lastfm.php');
require_once('inc.fitbit.php');

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
	<title>quantified.andreasherten.de</title>
	<meta name="description" content="">
	<meta name="viewport" content="width=device-width">

	<link rel="stylesheet" href="css/normalize.min.css">
	<link rel="stylesheet" href="css/main.css">
	<link rel="shortcut icon" href="favicon.png"> 
	<link rel="apple-itouch-icon" href="favicon.png">

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
		div.keypresses, div.clicks, div.plays {
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
			font-family: "FontAwesome";
			content: "\f11c";
			bottom: 3px;
		}
		.number.icon-plays:before {
			font-family: "FontAwesome";
			content: "\f001";
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
		#graph {
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
			<span class="number icon-clicks" title="<?php echo $lastClicks ?> clicks with my mouse yesterday."><?php echo $lastClicks ?></span>
		</div>
		<div class="plays">
			<span class="number icon-plays" title="<?php echo $yesterdaysPlays ?> songs listened to yesterday."><?php echo $yesterdaysPlays ?></span>
		</div>
		<div class="chart">
			<h1 id="history"><i class="fa fa-toggle-down"></i>History (Steps)</h1>
			 <div id="graph" style="min-width: 600px; height: 250px;"></div>
		</div>
		<div class="about">
			<h1><i class="fa fa-toggle-down"></i>About</h1>
			<div class="text-about">
				<p>Above numbers are the steps and stairs I walked yesterday (tracked by my Fitbit), as well as the keys I pressed and the mouseclicks I made (tracked by Whatpulse). If you see a boring <em>No</em> above, probably something went wrong. The graph shows the distribution of walked steps of the last nine days.<br/>
				This project is part of my <a href="http://www.andisblog.de/?s=quantified+self">Quantified Self studies</a>.
				</p>
				<p>The code to this project (including Fitbit-Api→SQLite-DB in Python as well as the PHP code running what you currently see) is <a href="https://github.com/AndiH/QuantifiedSelf/">available at Github</a>. Check it out. There's lots of other stuff there, partly in development.</p>
			</div>
	</div>

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
	<script>window.jQuery || document.write('<script src="js/vendor/jquery-1.10.1.min.js"><\/script>')</script>
	<script src="//code.jquery.com/ui/1.10.3/jquery-ui.js"></script>

	<script src="js/plugins.js"></script>
	<script src="js/main.js"></script>
	
	<script src="js/highcharts.js"></script>
	<script src="js/modules/exporting.js"></script>

	<script type="text/javascript">
	var stepColor = '#75b1dc';
	var floorColor = '#959cdc';
	var chartData = {
        chart: {
        	type: 'spline',
            zoomType: 'x',
            spacingRight: 20
        },
        title: {
/*                 text: 'Steps Walked' */
			text: null
        },
/*
        subtitle: {
            text: 'During last nine days. Also: Floors.'
        },
*/
        xAxis: {
            categories: <?php echo $jsonHistoryDates ?>,
        },
        yAxis: [{
            title: {
                text: '# Steps',
                style: {
                	color: stepColor
                }
            },
            labels: {
	            style: {
		            color: stepColor
	            }
            },
            min: 0,
            gridLineColor: '#eeeeee',
            gridLineWidth: 1
        }, {
            title: {
	            text: '# Floors',
	            style: {
		            color: floorColor
	            }
            },
            labels: {
	            style: {
		            color: floorColor
	            }
            },
            opposite: true,
            min: 0,
            gridLineWidth: null
        }],
        tooltip: {
            enabled: true,
        },
		plotOptions: {
			spline: {
				marker: {
					lineColor: '#FFFFFF',
                    lineWidth: 1,
				}
			}
		},
        series: [{
        	yAxis: 0,
            name: 'Steps',
            data: <?php echo $jsonHistorySteps ?>,
            color: stepColor
        }, {
        	yAxis: 1,
            name: 'Floors',
            data: <?php echo $jsonHistoryFloors ?>,
            color: floorColor
        }],
        
        navigation: {
            buttonOptions: {
                symbolStroke: '#EEE'
            }
        },
        legend: {
	        borderColor: null
        },
        credits: {
            enabled: false
        }
    };
		
	var firstRun = true;
	$(".chart #history").click(function() {
		if (firstRun) {
			$('#graph').highcharts(chartData);
			firstRun = false;
		} 
		$("#graph").toggle("blind");
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
