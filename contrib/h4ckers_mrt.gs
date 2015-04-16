function callRemoteJSONAPI(url) {
    var response = UrlFetchApp.fetch(url)
    var json = response.getContentText();
    var data = JSON.parse(json);
    // Logger.log(data);
    return data;
}

function getPossibleRouteStations(depart, arrive) {
  url = "http://xxx.com/api/possible/" + depart + "/" + arrive;

  return callRemoteJSONAPI(url);
}

function countStations() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet1 = ss.getSheetByName("Form Responses 1");
    var sheet2 = ss.getSheetByName("Form Responses 2");

    var data = sheet1.getDataRange().getValues();
  
    // counting stations  
    var station_count = {};
    for (var i = 1; i < data.length; i++) {    
        stations = data[i][4].split(",");
        for (var j = 0; j < stations.length; j++) {
            if (station_count[stations[j]]) {
                station_count[stations[j]] += 1;
            } else {
                station_count[stations[j]] = 1;
            }
        }
    }
  
    // save to sheet 2
    var i = 2;
    for(var key in station_count) {
        sheet2.getRange("A"+i).setValue(key);
        sheet2.getRange("B"+i).setValue(station_count[key]);
      
        i = i+1;
    }
  
    //Logger.log(station_count);
  
    return station_count;
}

function onFormSubmit() {
    var sheet = SpreadsheetApp.getActiveSheet();
    var data = sheet.getDataRange().getValues();

    // loop all row  
    for (var i = 1; i < data.length; i++) {
        // if no route station result
        if(!data[i][4])
        {
            var depart = data[i][2]
            var arrive = data[i][3]
            
            stations = getPossibleRouteStations(depart, arrive);
            stations = stations.join();
          
            // write result
            sheet.getRange("E"+i).offset(1, 0).setValue(stations);
        }
    }

    countStations();
}

// chart will auto update value fom sheet data
/*
function drawChart() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Form Responses 2");
  
    var station_count = countStations();
    // Logger.log(station_count);

    var chart = sheet.newChart()
        .setChartType(Charts.ChartType.BAR)
        .addRange(sheet.getRange('A1:B99'))  // x data, y data
        .setPosition(4, 4, 0, 0)
        .build();

    sheet.insertChart(chart);
}
*/
