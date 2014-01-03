<?php
$conn = mysql_connect($dbhost, $dbuser, $dbpass);
/*
if(! $conn) {
  die('Could not connect: ' . mysql_error());
}
*/

mysql_select_db('quantified');

$sql = 'SELECT * FROM Computerinput';

$retval = mysql_query( $sql, $conn );
/*
if(! $retval) {
  die('Could not get data: ' . mysql_error());
}
*/

$masterArray = array();

while($row = mysql_fetch_array($retval, MYSQL_ASSOC)) {
     $masterArray[$row['Date']] = array($row['Keystrokes'],$row['Mouseclicks']);
} 
mysql_close($conn);


$yesterdaysData = $masterArray[$yesterday];
$lastKeys = $lastClicks = "No";
$lastKeys = $yesterdaysData[0];
$lastClicks = $yesterdaysData[1];
?>