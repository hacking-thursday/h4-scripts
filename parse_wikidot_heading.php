<?php
error_reporting( 0 );
define( 'WIKIDOT_ROOT', dirname(__FILE__).'/3rd/wikidot');
//require_once( '/home/live/Programming/wikidot/lib/Text_Wiki/Text/Wiki.php' );
require_once( WIKIDOT_ROOT.'/php/utils/WikiTransformation.php' );
require_once( WIKIDOT_ROOT.'/php/utils/WDStringUtils.php' );

function get_opt_val( $options, $short_opt, $long_opt, $default ){
	$ret_data = NULL;

	if( $options[$long_opt] ){
		$ret_data = $options[$long_opt];
	}
	else if( $options[$short_opt] ){
		$ret_data = $options[$short_opt];
	}
	else{
		$ret_data = $default;
	}

	return $ret_data;
}

$shortopts = "";
$longopts  = array();
// 檔案路徑
{
	$shortopts .= "f:";  
	array_push( $longopts, "file:" );
}
$options = getopt($shortopts, $longopts);

$file_path = get_opt_val( $options, "f", "file", "" );

$wiki = new Text_Wiki();
$content = file_get_contents( $file_path );
$wiki->transform( $content, 'Xhtml');
$res = $wiki->getTokens( "Heading" );
foreach( $res as $item ){
	$type = $item[1]["type"];
	if ( $type == "start" ){
		$text = $item[1]["text"];
		echo $text."\n";
	}
}

?>
