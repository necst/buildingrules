var triggerPortions = 1;
var maxTriggerPortions = 5;

function updatePriority(value)
{
	priorityTextBox = document.getElementById('priorityTextBox');
	priorityTextBox.value = value;
}

function updateActionBlind(value)
{
	actionBlindTextBox = document.getElementById('actionBlindText');
	actionBlindTextBox.value = value + "%";

	compose();
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function goCdegree(){
	this.location = "index_celsius.html?usrcat=" + getParameterByName('usrcat')
}

function goFdegree(){
	this.location = "index.html?usrcat=" + getParameterByName('usrcat')
}


function show(elementId)
{
	document.getElementById(elementId).style.display = "block";
}

function hide(elementId)
{
	document.getElementById(elementId).style.display = "none";
}

function hideAllTriggerSubBox(groupId)	
{

	hide('temperature_box_' + groupId);
	hide('time_box_' + groupId);
	hide('day_box_' + groupId);
	hide('date_box_' + groupId);	
}

function hideAllActionSubBox()
{
	hide('action_temperature_box');
	hide('action_humidity_box');
	hide('action_blind_box');
}

function getTriggerCategory(triggerText)
{

	if (triggerText == "room temperature is between") return "TEMPERATURE";
	if (triggerText == "external temperature is between") return "TEMPERATURE";
	if (triggerText == "time is between") return "TIME";
	if (triggerText == "the date is between") return "DATE";
	if (triggerText == "today is") return "DAY";

	return "DEFAULT";
}

function getActionCategory(actionText)
{

	if (actionText == "Select an action") return "NOT_VALID";
	if (actionText == "set temperature between") return "TEMPERATURE";
	if (actionText == "set humidity between") return "HUMIDITY";
	if (actionText == "set blind to") return "BLIND";

	return "DEFAULT";
}


function triggerSelected(groupId)
{

	triggerBox = document.getElementById("trigger_" + groupId)
	triggerText = triggerBox.options[triggerBox.selectedIndex].text;

	hideAllTriggerSubBox(groupId);

	triggerCategory = getTriggerCategory(triggerText);

	if (triggerCategory == "TEMPERATURE")	
	{
		show('temperature_box_' + groupId);
	}

	if (triggerCategory == "TIME")	
	{
		show('time_box_' + groupId);
	}

	if (triggerCategory == "DATE")	
	{
		show('date_box_' + groupId);
	}

	if (triggerCategory == "DAY")	
	{
		show('day_box_' + groupId);
	}


}

function actionSelected()
{
	actionBox = document.getElementById("action_0");
	actionText = actionBox.options[actionBox.selectedIndex].text;

	actionCategory = getActionCategory(actionText);

	hideAllActionSubBox();

	
	if (actionCategory == "DEFAULT")
	{
		compose();
	}

	if (actionCategory == "TEMPERATURE")
	{
		show('action_temperature_box');
	}

	if (actionCategory == "HUMIDITY")
	{
		show('action_humidity_box');
	}

	if (actionCategory == "BLIND")
	{
		show('action_blind_box');
	}


}



function goToConfirmPage() {
    setTimeout(function () {
        this.location = "thanks.html"
    }, 4000);
}

function compose()
{

	antecent = "if ";

	for (var i=0; i < triggerPortions; i++){

		groupId = i;

		triggerBox = document.getElementById("trigger_" + groupId);
		temperatureFrom = document.getElementById("temperature_from_" + groupId);
		temperatureTo = document.getElementById("temperature_to_" + groupId);
		timeFrom = document.getElementById("time_from_" + groupId);
		timeTo = document.getElementById("time_to_" + groupId);
		dateDayFrom = document.getElementById("date_day_from_" + groupId);
		dateMonthFrom = document.getElementById("date_month_from_" + groupId);
		dateDayTo = document.getElementById("date_day_to_" + groupId);
		dateMonthTo = document.getElementById("date_month_to_" + groupId);
		day = document.getElementById("day_" + groupId);
		triggerText = triggerBox.options[triggerBox.selectedIndex].text;
		
		triggerCategory = getTriggerCategory(triggerText);

		if (triggerCategory == "DEFAULT"){
			antecent += triggerText + ", ";
		}

		if (triggerCategory == "TEMPERATURE")
		{
			tempFromText = temperatureFrom.options[temperatureFrom.selectedIndex].text;
			tempToText = temperatureTo.options[temperatureTo.selectedIndex].text;
			antecent += triggerText + " " + tempFromText + " and " + tempToText + ", ";
		}

		if (triggerCategory == "TIME")
		{
			timeFromText = timeFrom.options[timeFrom.selectedIndex].text;
			timeToText = timeTo.options[timeTo.selectedIndex].text;
			antecent += triggerText + " " + timeFromText + " and " + timeToText + ", ";
		}

		if (triggerCategory == "DATE")
		{
			dateDayFromText = dateDayFrom.options[dateDayFrom.selectedIndex].text;
			dateMonthFromText = dateMonthFrom.options[dateMonthFrom.selectedIndex].text;
			dateDayToText = dateDayTo.options[dateDayTo.selectedIndex].text;
			dateMonthToText = dateMonthTo.options[dateMonthTo.selectedIndex].text;

			antecent += triggerText + " " + dateDayFromText + "/" + dateMonthFromText + " and " + dateDayToText + "/" + dateMonthToText + ", ";
		}

		if (triggerCategory == "DAY")
		{
			dayText = day.options[day.selectedIndex].text;
			antecent += triggerText + " " + dayText + ", ";
		}

	}

	antecent = antecent.slice(0, -2);

	actionBox = document.getElementById("action_0");

	humiditySetpointMinBox = document.getElementById("humiditySetpoint_min");
	humiditySetpointMaxBox = document.getElementById("humiditySetpoint_max");
	tempSetpointMinBox = document.getElementById("tempSetpoint_min");
	tempSetpointMaxBox = document.getElementById("tempSetpoint_max");
	actionBlindTextBox = document.getElementById("actionBlindText");
	

	actionText = actionBox.options[actionBox.selectedIndex].text;
	
	actionCategory = getActionCategory(actionText);
	consequent = ""


	if (actionCategory == "DEFAULT")
	{
		consequent = actionText;
	}

	if (actionCategory == "TEMPERATURE")
	{
		consequent = actionText + " " + tempSetpointMinBox.value + " and " + tempSetpointMaxBox.value;
	}

	if (actionCategory == "HUMIDITY")
	{
		consequent = actionText + " " + humiditySetpointMinBox.value + " and " + humiditySetpointMaxBox.value;
	}

	if (actionCategory == "BLIND")
	{
		consequent = actionText + " " + actionBlindTextBox.value;
	}


	ruleBody = document.getElementById('ruleBody');
	ruleBody.value = antecent + " then " + consequent


}


function updateHumiditySetpoint()
{

	unit = "%"
	
	desiredValueBox = document.getElementById("desired_humidity");
	rangeValueBox = document.getElementById("accepted_humidity_range");
	humiditySetpointMinBox = document.getElementById("humiditySetpoint_min");
	humiditySetpointMaxBox = document.getElementById("humiditySetpoint_max");

	maxAllowedTemp = desiredValueBox.max;
	minAllowedTemp = desiredValueBox.min;

	desiredValue = desiredValueBox.value;
	rangeValue = rangeValueBox.value;

	humiditySetpointMin = parseInt(desiredValue) - parseInt(rangeValue);
	humiditySetpointMax = parseInt(desiredValue) + parseInt(rangeValue);

	orangeArea = humiditySetpointMin - minAllowedTemp;
	orangeArea_perc = parseInt(rangeValue) * 5;

	
	document.getElementById("humiditySetpoint_bar_value").width = orangeArea_perc + "%" ;
	
	document.getElementById("humiditySetpoint_bar_min").innerHTML = humiditySetpointMin + unit;
	document.getElementById("humiditySetpoint_bar_value").innerHTML = desiredValue + unit;
	document.getElementById("humiditySetpoint_bar_max").innerHTML = humiditySetpointMax + unit;
	
	humiditySetpointMinBox.value = humiditySetpointMin + unit;
	humiditySetpointMaxBox.value = humiditySetpointMax + unit;

	compose();


}

function updateTemperatureSetpoint()
{

	unit = "F"
	
	desiredValueBox = document.getElementById("desired_temperature");
	rangeValueBox = document.getElementById("accepted_temperature_range");
	tempSetpointMinBox = document.getElementById("tempSetpoint_min");
	tempSetpointMaxBox = document.getElementById("tempSetpoint_max");

	maxAllowedTemp = desiredValueBox.max;
	minAllowedTemp = desiredValueBox.min;

	desiredValue = desiredValueBox.value;
	rangeValue = rangeValueBox.value;

	tempSetpointMin = parseInt(desiredValue) - parseInt(rangeValue);
	tempSetpointMax = parseInt(desiredValue) + parseInt(rangeValue);

	orangeArea = tempSetpointMin - minAllowedTemp;
	orangeArea_perc = parseInt(rangeValue) * 5;

	
	document.getElementById("tempSetpoint_bar_value").width = orangeArea_perc + "%" ;
	
	document.getElementById("tempSetpoint_bar_min").innerHTML = tempSetpointMin + unit;
	document.getElementById("tempSetpoint_bar_value").innerHTML = desiredValue + unit;
	document.getElementById("tempSetpoint_bar_max").innerHTML = tempSetpointMax + unit;
	
	tempSetpointMinBox.value = tempSetpointMin + unit;
	tempSetpointMaxBox.value = tempSetpointMax + unit;

	compose();


}

function ruleBodyAlert()
{
	alert("Please use the 'Rule Composer' below to create your rule! :) ")
	
}

function addTriggerPortion()
{
	if (triggerPortions < maxTriggerPortions)
	{
		show("triggerPortion_" + triggerPortions);
		triggerPortions = triggerPortions + 1;
	} else {
		alert("You reached the maximum number of rule triggers per rule!")
	}
}

function removeTriggerPortion()
{
	if (triggerPortions > 1)
	{
		triggerPortions = triggerPortions - 1;
		hide("triggerPortion_" + triggerPortions);
	} else {
		alert("You have to insert at least one trigger per rule!")
	}
}


function init()
{

	hideAllTriggerSubBox(0);
	
	for (var i=1; i < maxTriggerPortions; i++){
		hideAllTriggerSubBox(i);
		hide("triggerPortion_" + i)
	}

	hideAllActionSubBox();
}


	