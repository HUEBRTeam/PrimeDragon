<?php

if(!empty($_REQUEST["accesscode"]))	{
	$ac = str_replace(".","",$_REQUEST["accesscode"]);
	$ac = str_replace(" ","",$ac);
	$ac = str_replace(";","",$ac);
	$ac = addslashes($ac);
	$bot = shell_exec("python bot.py \"".$ac."\"");
	echo nl2br($bot);
}else
	echo "No Access Code Provided!";
?>
