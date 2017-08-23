<!DOCTYPE html>
<head>
	<title>Level:Easy</title>

<style>
div#test{ border:#000 1px solid; padding:10px 40px 40px 40px; text-align: justify;}
</style>
<script>
var pos = 0, test, test_status, question, choice, choices, chA, chB, chC,chD, correct = 0;
var questions = [
    [ "What is 17 - 4?", "12", "13", "16","15", "B" ],
	[ "What is 20 + 9?", "27", "13", "29","15" ,"C" ],
	[ "What is 7 x 3?", "21", "24", "25","32", "A" ],
	[ "What is 8 / 2?", "10", "2", "4","5" ,"C" ],
	[ "What is 9 / 3?", "10", "2", "3","5" ,"C" ]
];
function _(x){
	return document.getElementById(x);
}

function renderQuestion(){
	test = _("test");
	if(pos >= questions.length){

		test.innerHTML = "<h2>You got "+correct+" of "+questions.length+" questions correct</h2><br/>";
		_("test_status").innerHTML = "Test Completed";

		pos = 0;
		correct = 0;
		return false;

	}
	


	_("test_status").innerHTML = "Question "+(pos+1)+" of "+questions.length;
	question = questions[pos][0];
	chA = questions[pos][1];
	chB = questions[pos][2];
	chC = questions[pos][3];
	chD = questions[pos][4];
	test.innerHTML = "<h3>"+question+"</h3>";
	test.innerHTML += "<input type='radio' name='choices' value='A'> "+chA+"<br>";
	test.innerHTML += "<input type='radio' name='choices' value='B'> "+chB+"<br>";
	test.innerHTML += "<input type='radio' name='choices' value='C'> "+chC+"<br>";
	test.innerHTML += "<input type='radio' name='choices' value='B'> "+chD+"<br><br>";
	test.innerHTML += "<button onclick='checkAnswer()'>Submit Answer</button>";


}
	
function checkAnswer(){
	choices = document.getElementsByName("choices");
	for(var i=0; i<choices.length; i++){
		if(choices[i].checked){
			choice = choices[i].value;
		}
	}
	if(choice == questions[pos][5]){
		correct++;
	}

	pos++;

	renderQuestion();
}
window.addEventListener("load", renderQuestion, false);
</script>


</head>
<?php


$dateFormat = "d F Y -- g:i a";

$targetDate = time() + (1*60);//Change the 25 to however many minutes you want to countdown

$actualDate = time();

$secondsDiff = $targetDate - $actualDate;

$remainingDay    = floor($secondsDiff/60/60/24);

$remainingHour  = floor(($secondsDiff-($remainingDay*60*60*24))/60/60);

$remainingMinutes = floor(($secondsDiff-($remainingDay*60*60*24)-($remainingHour*60*60))/60);

$remainingSeconds = floor(($secondsDiff-($remainingDay*60*60*24)-($remainingHour*60*60))-($remainingMinutes*60));

$actualDateDisplay = date($dateFormat,$actualDate);

$targetDateDisplay = date($dateFormat,$targetDate);

?>

<body>
		<h1 style="text-align: center;background-color:Grey; font-family: Comic Sans Ms; color: Black;  margin-top: 0">Welcome To Level: Easy</h1>
		<script type="text/javascript">

  var minutes = <?php echo $remainingMinutes; ?> 

  var seconds = <?php echo $remainingSeconds; ?>

function setCountDown ()

{

  seconds--;

  if (seconds < 0){

      minutes--;

      seconds = 30

  }

  if (minutes < 0){

      hours--;

      minutes = 59

  }

  document.getElementById("remain").innerHTML = "Time:" + seconds+" seconds";

  SD=window.setTimeout( "setCountDown()", 1000 );

  if (minutes == '00' && seconds == '00') { seconds = "00"; window.clearTimeout(SD);

        window.alert("Time is up. Press OK to continue."); // change timeout message as required

          window.location = "main.php" // Add your redirect url

  }

 

}

</script>
<body onload="setCountDown();">

 <div id="remain"><?php echo "$remainingSeconds seconds";?></div>

 
</div>
<h2 id="test_status"></h2>
<div id="test"></div>
</body>
</html>