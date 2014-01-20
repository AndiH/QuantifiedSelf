<?php

$dayBeforeYesterday = strtotime(date('Y-m-d', strtotime("-2 days")));

$sql = 'SELECT * FROM `LastfmLIGHT` WHERE date='.$yesterday.' OR date='.$dayBeforeYesterday.' ORDER BY date DESC';

$retval = mysql_query( $sql, $conn );
/*
if(! $retval) {
  die('Could not get data: ' . mysql_error());
}
*/

$lastfmArray = array();

while($row = mysql_fetch_array($retval, MYSQL_ASSOC)) {
     $lastfmArray[$row['date']] = $row['totalplays'];
} 

$yesterdaysPlays = "Nothing";
$yesterdaysPlays = $lastfmArray[$yesterday] - $lastfmArray[$dayBeforeYesterday];
?>