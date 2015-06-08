<?php

if(!empty($_REQUEST["accesscode"]))	{
	$ac = str_replace(".","",$_REQUEST["accesscode"]);
	$ac = str_replace(" ","",$ac);
	$ac = str_replace(";","",$ac);
	$ac = addslashes($ac);
	$profile = shell_exec("python getprofile.py \"".$ac."\"");
	echo $profile;
}else
	echo "{\"name\":\"No Access Code\",\"avatar\":1}";
?>
