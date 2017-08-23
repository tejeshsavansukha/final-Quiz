<!DOCTYPE html>
<html>
<head>
	<title>Main Page</title>
</head>
<body>
	<div style="height: 400px">	<h1 style="text-align: center;background-color:Grey; font-family: Comic Sans Ms; color: Black;  margin-top: 0">Welcome To Quiz Contest</h1>
		
		<div style="text-align: center; margin-top: 80px;">
		<h3 style="text-align: center;""> Select The Quiz Level</h3>
		  <form id="link" method="POST">
		<select style="width:200px; height: 30px;" name="opt" >
		<option >Select Category</option>
		<option class="Easy" value="Easy">Easy</option>
		<option class="Medium" value="Medium">Medium</option>
		<option class="Hard" value="Hard">Hard</option>
		</select>


		</div>
		<div style="text-align: center; margin-top: 80px">
		 <input class="SubmitButton" type="submit" name="submit" value="Submit" style="font-size:20px; "/>
		</form>
		</div>
	
	<?php
if (isset($_POST['submit']))
{
    if (isset($_POST['opt']))
    {
        if ($_POST['opt'] == 'Easy') { header('Location: easy.html'); }
        elseif ($_POST['opt'] == 'Medium') { header('Location: medium.html'); }
         elseif ($_POST['opt'] == 'Hard') { header('Location: hard.html'); }
        
    }
}
	?></div>
	<footer style="background-color:Grey; font-family: Comic Sans Ms; text-align: center; color: Black; position: fixed; width: 1350px; height: 200px;margin-top: 50px; font-size: 18px; font-style: bold">Footer Area</footer>
</body>
</html>
