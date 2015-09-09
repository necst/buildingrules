
ruleCategories = [];

function hideClass(className)
{
	var elements = document.getElementsByClassName(className), i;

	for (var i = 0; i < elements.length; i ++) {
	    elements[i].style.display = 'none';
	}
}

function showClass(className)
{
	var elements = document.getElementsByClassName(className), i;

	for (var i = 0; i < elements.length; i ++) {
	    elements[i].style.display = 'block';
	}
}

function filterByRuleCategory(roomName, ruleCategory)
{

	if (ruleCategory == "SHOWALL")
	{
		for (var i = 0; i < ruleCategories.length; i ++)
		{
			showClass('rule_' + roomName + "_" + ruleCategories[i]);
			document.getElementById("btn_" + roomName + "_" + ruleCategories[i]).setAttribute("class", "btn");
		}
		
		document.getElementById("btn_" + roomName + "_SHOWALL").setAttribute("class", "btn active");

	} else {

		document.getElementById("btn_" + roomName + "_SHOWALL").setAttribute("class", "btn");

		for (var i = 0; i < ruleCategories.length; i ++)
		{
			hideClass('rule_' + roomName + "_" + ruleCategories[i]);
			document.getElementById("btn_" + roomName + "_" + ruleCategories[i]).setAttribute("class", "btn");
		}
		showClass('rule_' + roomName + "_" + ruleCategory);
		
		document.getElementById("btn_" + roomName + "_" + ruleCategory).setAttribute("class", "btn active");
	}

}


function show(elementId)
{
	document.getElementById(elementId).style.display = "block";
}

function hide(elementId)
{
	document.getElementById(elementId).style.display = "none";
}

function hideAll()
{
	hide("btnShowMaps");
	hide("btnHideMaps");
	hide("btnShowThMaps");
	hide("btnShowAccMaps");
	hide("accessMap");
	hide("thZoneMap");
}

function hideMaps()
{
	hideAll()
	show("btnShowMaps");

}

function showMaps()
{
	hideAll();
	showAccessMaps();
}

function showAccessMaps()
{
	hideAll();
	show("accessMap");
	show("btnShowThMaps");
	show("btnHideMaps");
}

function showThermalZoneMaps()
{
	hideAll();
	show("thZoneMap")
	show("btnShowAccMaps");
	show("btnHideMaps");
}

function hideMTurk()
{
	hide('mturkPanel');
	hide('btnHideMTurk');
	show('btnShowMTurk');
}

function showMTurk()
{
	show('mturkPanel');
	hide('btnShowMTurk');
	show('btnHideMTurk');
}

function init()
{
	showAccessMaps();
	showMTurk();
}
