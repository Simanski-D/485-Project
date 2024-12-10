const csvtojson = import('csvtojson'); 
const mysql = import("mysql");
import * as csvtojson from 'https://cdn.jsdelivr.net/npm/csvtojson@2.0.10/dist/csvtojson.browser.min.js';

// Database credentials 
const hostname = "wayne.cs.uwec.edu", 
    username = "DENNERKW5831", 
    password = "7Q155UGZ", 
    databsename = "cs485group1"
    // not sure if need port = "3306"  

  
// Establish connection to the database 
let con = mysql.createConnection({ 
    host: hostname, 
    user: username, 
    password: password, 
    database: databsename, 
}); 
  
con.connect((err) => { 
    if (err) return console.error( 
            'error: ' + err.message);
});


// input log path passing
fileInput.addEventListener('change', (event) => {
    const fileInput = document.getElementById('file');

    // Check if a file has been selected
    const files = fileInput.files; 

    if (files.length > 0) {
        // Get the file name of the first file
        const fileName = files[0].name;
        localStorage.setItem('fileName', fileName);  // Store the file name in localStorage
        console.log('Input File name saved to localStorage:', fileName);
    }
    const fileName = localStorage.getItem('fileName');
    csvtojson().fromFile(fileName).then(source => { 
  
        // Fetching the data from each row  
        // and inserting to the table "sample" 
        //https://www.geeksforgeeks.org/how-to-import-data-from-csv-file-into-mysql-table-using-node-js/

        for (var i = 0; i < source.length; i++) { 
            var Username = source[i]["user.full_name"], 
                Time = source[i]["@Timestamp"], 
                Lon = source[i]["client.geo.location.lon"], 
                Lat = source[i]["client.geo.location.lat"] ,
                Outcome = source[i]["event.outcome"]
      
            var insertStatement =  
            `INSERT INTO input_logs values(?, ?, ?, ?, ?)`; 
            var items = [Username, Time, Lon, Lat, Outcome]; 
      
            // Inserting data of current row 
            // into database 
            con.query(insertStatement, items,  
                (err, results, fields) => { 
                if (err) { 
                    console.log( 
        "Unable to insert item at row ", i + 1); 
                    return console.log(err); 
                } 
            }); 
        } 
        console.log( 
    "All items stored into database successfully"); 
    }); 
});


// output log path passing
document.getElementById("submit").onclick = function(){
    const fileInput = document.getElementById('file');

    // Check if a file has been selected
    const files = fileInput.files; 

    if (files.length > 0) {
        // Get the file name of the first file
        const outputFileName = files[0].name;
        const outputChoppedFilename = outputFileName.substring(0, fileName.lastIndexOf('.'));
        const fileName2 = outputChoppedFilename + "_predicted.csv";
        localStorage.setItem('fileName2', fileName2);  // Store the file name in localStorage
        console.log('Output File name saved to localStorage:', fileName2);
    }
}