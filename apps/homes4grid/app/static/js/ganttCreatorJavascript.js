
var slotsNumber = {}
var currentSlots = {}


function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function show(elementId)
{
	document.getElementById(elementId).style.display = "block";
}

function hide(elementId)
{
	document.getElementById(elementId).style.display = "none";
}

function addSlot(appliance)
{
	
	show("ts_" + appliance + '_timeslot_' + currentSlots[appliance] );
	if (currentSlots[appliance]  < slotsNumber[appliance]) currentSlots[appliance]  += 1;
}

function removeSlot(appliance)
{
	
	if (currentSlots[appliance]  > 1) currentSlots[appliance]  -= 1;
	hide("ts_" + appliance + '_timeslot_' + currentSlots[appliance] );
	
}

function sendValues(appliance){

	gantt = {}
	gantt[appliance] = []


	for (var i=0; i< currentSlots[appliance] ; i++)
	{
		gantt[appliance][i] = {}
		gantt[appliance][i]["elastic"] = "TRUE"
		gantt[appliance][i]["from"] = document.getElementById("from_" + i).value;
		gantt[appliance][i]["to"] = document.getElementById("to_" + i).value;

	}
	//document.getElementById("textToSubmitBox").value = JSON.stringify(gantt);
	//document.getElementById("mainForm").submit();
	alert(JSON.stringify(gantt));

}

function hideApplianceSettings(appliance)
{
	hide("settings_" + appliance);
}

function hideApplianceTimeslots(appliance)
{
	hide("timeslots_" + appliance)
}

function hideApplianceMenu(appliance)
{
	hide("menu_" + appliance);
}

function showApplianceSettings(appliance)
{
	show("settings_" + appliance);
	hide("timeslots_" + appliance);
}

function showApplianceTimeslots(appliance)
{
	show("timeslots_" + appliance)
	hide("settings_" + appliance);
}

function showApplianceMenu(appliance)
{
	show("menu_" + appliance);
}


function initApplianceTimeslots(appliance)
{
	slotsNumber[appliance] = 4;
	currentSlots[appliance] = 1;

	for (var i=1; i< slotsNumber[appliance]; i++)
	{
		hide("ts_" + appliance + "_timeslot_" + i);		
	}

}

function initAppliance(appliance)
{	
	initApplianceTimeslots(appliance);
	hideApplianceSettings(appliance);
	hideApplianceMenu(appliance);

}


