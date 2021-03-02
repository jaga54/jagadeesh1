<?php
session_start();
if($_POST['formsubmitted'])
{
 $_SESSION['formsubmitted'] = 'true';
}
if(isset($_SESSION['formsubmitted']))
{
 return false;
}
else
{
  return true;
}
?>