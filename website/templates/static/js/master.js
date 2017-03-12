// Numbers:
// http://stackoverflow.com/questions/8677805/formatting-numbers-decimal-places-thousands-separators-etc-with-css
// master_hostname = '127.0.0.1:8000'

function numberFormat(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function x1000(int_array) {
  for(var i = 0; i < int_array.length; i++){
    int_array[i] = int_array[i] * 1000;
  }
  return int_array;
}

// Date:
// http://stackoverflow.com/questions/15411833/using-moment-js-to-convert-date-to-string-mm-dd-yyyy
function dateToMMYYYY(date){
  // Always returning Jan 1970:
  // http://stackoverflow.com/questions/35093347/moment-js-amdateformat-always-returning-date-from-1970
  date = moment.unix(parseInt(date)).format('MMM YYYY');
  return date;
}

function dateToDetailedTime(date_array){
    for(var i = 0; i < date_array.length; i++){
        date_array[i] = moment.unix(date_array[i], 'YYYY-MM-DD HH:mm:ss')
    }
    return date_array
}

// String to JSON object:
// http://stackoverflow.com/a/4375715
function stringToJSON(strObj){
  var jsonObj = strObj.split(",");
  // var jsonObj = "Action, Super Power, Drama, Fantasy, Shounen,".split(",");

  // MUST use var i while looping!
  for (var i = 0; i < jsonObj.length; i++){
    jsonObj[i] = jsonObj[i].trim().replace(' ', '_').replace('-', '_');
  }
  return jsonObj;
  // return str;
  // return ["Action"," Police"," Psychological"," Supernatural"];
}

function removeNavProperties(navID, css_class) {
    $('#' + navID).removeClass(css_class);
    // alert('#' + navID + ':: ' + css_class);
}

function addNavProperties(navID, css_class) {
    navID = '#' + navID;
    $(navID).addClass(css_class);
    // if (navID === '#nav-home') {
    //   $(navID).attr('href', current_host);
    // }else if (navID === '#nav-stats') {
    //   $(navID).attr('href', current_host + 'stride_stats/');
    // }else if (navID === '#nav-recommender') {
    //   $(navID).attr('href', current_host + 'stride_recommender/');
    // }else if (navID === '#nav-about') {
    //   $(navID).attr('href', current_host + 'about/');
    // }
    // alert('#' + navID + ':: ' + css_class);
}

function addNavURL(navID){
  navID = '#' + navID;

  if (navID === '#nav-home') {
    $(navID).attr('href', current_host);
  }else if (navID === '#nav-stats') {
    $(navID).attr('href', current_host + '/stride_stats/');
  }else if (navID === '#nav-recommender') {
    $(navID).attr('href', current_host + '/stride_recommender/');
  }else if (navID === '#nav-about') {
    $(navID).attr('href', current_host);
  }
}
