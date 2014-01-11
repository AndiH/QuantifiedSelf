<?php

$today = strtotime('today');
$dates = array();
$queryString = "SELECT * FROM Fitbit";
$queryString = $queryString . ' where ';
$nOfHistoryDays = 10;
for ($i = 1; $i < $nOfHistoryDays; $i++) {
	$currentDate = strtotime('-' . $i . ' day', $today);
	array_push($dates, $currentDate);
	$queryString .= "(date = " . $currentDate . ") ";
	if ($i < ($nOfHistoryDays - 1 )) $queryString .= "OR ";
}

$historyQuery = mysql_query( $queryString, $conn );

/*
if(! $historyQuery) {
  die('Could not get data: ' . mysql_error());
}
*/

$historyFitbit = array();

while($row = mysql_fetch_array($historyQuery, MYSQL_ASSOC)) {
	$historyFitbit[$row['date']] = array($row['steps'], $row['floors']);
}

mysql_close($conn);

function convDate($d) {
	return date("d.m", $d);
}
function getFirstElement($i) {
	return $i[0];
}
function getSecondElement($i) {
	return $i[1];
}
$jsonHistoryDates = json_encode(array_map("convDate", array_keys($historyFitbit)));
$jsonHistorySteps = json_encode(array_map("getFirstElement", array_values($historyFitbit)));
$jsonHistoryFloors = json_encode(array_map("getSecondElement", array_values($historyFitbit)));

$lastSteps = $lastFloors = "No";
$lastSteps = $historyFitbit[$yesterday][0];
$lastFloors = $historyFitbit[$yesterday][1];
?>