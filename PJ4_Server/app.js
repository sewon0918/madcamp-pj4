// app.js

// [LOAD PACKAGES]
var express     = require('express');
let {PythonShell} = require('python-shell')
const path = require('path')
const {spawn} = require('child_process')
var app         = express();
var bodyParser  = require('body-parser');
var mongoose    = require('mongoose');

// [ CONFIGURE mongoose ]

// CONNECT TO MONGODB SERVER
var db = mongoose.connection;
db.on('error', console.error);
db.once('open', function(){
    // CONNECTED TO MONGODB SERVER
    console.log("Connected to mongod server");
});

mongoose.connect('mongodb://localhost/madcamp_finalweek');

// DEFINE MODEL
var Omok = require('./models/Omok');

// [CONFIGURE APP TO USE bodyParser]
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

function runScript(){
    return spawn('python', [
      "-u", 
      path.join('../', 'test.py'),
      "--foo", "some value for foo",
    ]);
}

const subprocess = runScript()
  
// print output of script
subprocess.stdout.on('data', (data) => {
    console.log(`data:${data}`);
});
subprocess.stderr.on('data', (data) => {
    console.log(`error:${data}`);
});
subprocess.stderr.on('close', () => {
    console.log("Closed");
});

// [CONFIGURE SERVER PORT]
var port = process.env.PORT || 8000;

// [CONFIGURE ROUTER]
var router = require('./routes/index')(app, Omok)

// [RUN SERVER]
var server = app.listen(port, function(){
    console.log("Express server has started on port " + port)
});

