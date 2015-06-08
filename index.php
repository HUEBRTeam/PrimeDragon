<html>
	<head>
		<title>PrimeDragon</title>
		<script src="js/jquery-1.11.3.min.js"></script>
		<script src="js/jquery.color-2.1.2.min.js"></script>
		<style type="text/css">
			body {
				background-color: black;
			}
			#dragon {
				background: url('bg.jpg');
				width: 800px;
				height: 467px;
				position: absolute;
				margin-left: 50%;
				left: -400px;
				text-align: center;
			}
			#profilename {
				color: white;
			}
			#profile {
				width: 116px;
				height: 140px;
				position: absolute;
				left: 10px;
				top: 10px;
				display: none;
			}
			#senddata {
				color: white;
				width: 500px;
				height: 100px;
				background-color: rgba(0,0,0,0.4);
				/*border: dashed 2px #FFFFFF;*/
				border: dashed 2px rgba(0,0,0,0);
				position: absolute;
				margin-left: 50%;
				left: -250px;
				top: 300px;
				-webkit-border-radius: 10px;
				-moz-border-radius: 10px;
				border-radius: 10px;
			}
		</style>
		<script>
			function dec2hex(i) {
			   return (i+0x10000).toString(16).substr(-2).toUpperCase();
			}
			function handleDragOver(e)	{
			    e.preventDefault();
			    e.stopPropagation();
			    //$("#senddata").css("border","dashed 2px #FFFFFF");
			    $("#senddata").stop(true).animate({
			    	backgroundColor: "rgba(0,0,0,0.8)",
			    	borderTopColor: 'rgba(255,255,255,1)', 
			    	borderLeftColor: 'rgba(255,255,255,1)', 
			    	borderRightColor: 'rgba(255,255,255,1)', 
			    	borderBottomColor: 'rgba(255,255,255,1)'
			    }, 300);
			    e.originalEvent.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
			}

			function handleDragOut(e)	{
			    e.preventDefault();
			    e.stopPropagation();
			    //$("#senddata").css("border","dashed 2px rgba(0,0,0,0)");
			    $("#senddata").stop(true).animate({
			    	backgroundColor: "rgba(0,0,0,0.4)",
			    	borderTopColor: 'rgba(0,0,0,0)', 
			    	borderLeftColor: 'rgba(0,0,0,0)', 
			    	borderRightColor: 'rgba(0,0,0,0)', 
			    	borderBottomColor: 'rgba(0,0,0,0)'
			    }, 300);
			}

			function resetlog()	{
				$("#senddata").html("");
			}

			function log(msg, toConsole)	{
				toConsole == toConsole === undefined ? true : false;

				if(toConsole)	
					console.log(msg);
				else
					$("#senddata").html($("#senddata").html()+msg+"<BR>");
			}

			function startBlock()	{
				$("#senddata").animate({
					"top" : "25px",
					"height" : "400px",
					"backgroundColor" : "rgba(0,0,0,0.8)"
				},500);
			}

			function pad(num, size) {
			    var s = num+"";
			    while (s.length < size) s = "0" + s;
			    return s;
			}

			function showProfile(avatar, name)	{
				$("#profileimage").attr("src", "http://www.piugame.com/piu.prime/_img/avatar/"+pad(avatar, 3)+".png");
				$("#profilename").html("<B>"+name+"</B>");
				$("#profile").fadeIn();
			}

			function handleFileSelect(e)	{
			    handleDragOut(e);
		        var files = e.originalEvent.dataTransfer.files; // FileList object.
  				if(files.length > 0)    {
			        resetlog();
			        startBlock();
			        log("Reading file "+files[0].name,false);
			        var reader = new FileReader();
			        reader.onload = (function(theFile) { return function(e) {
            				var savedata = new Uint8Array(e.target.result);
            				var ac = "";
            				if(savedata.length != 16)	{
            					log("Invalid prime.bin",false);
							    $("#senddata").on('dragover', handleDragOver);
							    $("#senddata").on('dragleave', handleDragOut);
							    $("#senddata").on('drop', handleFileSelect);
            					return;
            				}
            				for(var i=0;i<savedata.length;i++)	{
            					ac += dec2hex(savedata[i]);
            				}

            				log("Your accesscode: "+ac);
            				log("Getting profile data...");
            				$.getJSON("getprofile.php",{"accesscode":ac}, function(data) {
            					if(data.name !== undefined)	{	
            						if(data.name == "No Access Code")	
            							log("No access code provided!!!!<BR>Refresh the page and try again.");
            						else{
		            					log("Profile Name: "+data.name+" Avatar ID: "+data.avatar);
		            					showProfile(data.avatar, data.name);
		            					log("Adding 196605 PP to "+data.name+".<BR>Please wait, this should take a moment.");
		            					$.get("dobot.php",{"accesscode":ac}, function(data) {
		            						log(data);
		            					});
		            				}
	            				}else{
	            					log("Error getting profile! Refresh page and try again!");
	            				}
            				});
			        };})(files[0]);
			        reader.readAsArrayBuffer(files[0]); 
				}
			    $("#senddata").off('dragover');
			    $("#senddata").off('dragleave');
			    $("#senddata").off('drop');
			}

			$( document ).ready(function() {
			    $("#senddata").on('dragover', handleDragOver);
			    $("#senddata").on('dragleave', handleDragOut);
			    $("#senddata").on('drop', handleFileSelect);
			});
		</script>
	</head>
	<body><BR>
		<div id="dragon">
			<div id="profile">
				<img id="profileimage" style="width: 116px; height: 116px;"/>
				<BR>
				<span id="profilename">PrimeDragon</span>
			</div>
			<div id="senddata"><BR><BR>
				<B>Thrown your prime.bin file here</B>
			</div>
		</div>
	</body>
</html>	