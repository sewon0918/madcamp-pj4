var express     = require('express');
const path = require('path')
const {spawn} = require('child_process')
var app         = express();

function runScript(){
    return spawn('python', [
      "-u", 
      path.join('../', 'test.py'),
      "--foo", "some value for foo",
    ]);
}
  
const subprocess = runScript()

module.exports = function(app, Omok)
{
    app.get('/api/run', function (req, res) {
        const subprocess = runScript()
        // res.set('Content-Type', 'text/plain');
        subprocess.stdout.pipe(res)
        // app.post('/api/run', function (req, res) {
        //     var omok = new Omok();
        //     omok.id = x
        //     omok.xy = x
        //     omok.save(function(err){
        //         if(err){
        //             console.error(err);
        //             res.json({result: 0});
        //             return;
        //         }
        //         res.json({result: 1});
        //     });
        // })
    })
    app.post('/api/run', function (req, res) {
        const subprocess = runScript()
        //subprocess.stdout.pipe(res)
        var omok = new Omok();
        // omok.id = subprocess.stdout.pipe(res)
        omok.xy = subprocess.stdout.pipe(res)
        omok.save(function(err){
            if(err){
                console.error(err);
                res.json({result: 0});
                return;
            }
            res.json({result: 1});
        });
    })
    
    
    // GET ALL BOARD
    app.get('/api/omok', function(req,res){
        Omok.find({},  function(err, omok){
            if(err) return res.status(500).send({error: 'database failure'});
            res.json(omok);
        })
    });

    // ADD 
    app.post('/api/omok', function(req, res){
        var omok = new Omok();
        omok.id = req.body.id;
        omok.xy = req.body.xy;
        omok.save(function(err){
            if(err){
                console.error(err);
                res.json({result: 0});
                return;
            }
            res.json({result: 1});
        });
    });

    // DELETE BOARD
    app.delete('/api/omok', function(req, res){
        Omok.deleteMany({}, function(err, output){
            if(err) return res.status(500).json({ error: "database failure" });

            // ( SINCE DELETE OPERATION IS IDEMPOTENT, NO NEED TO SPECIFY )
            // if(!output.result.n) return res.status(404).json({ error: "book not found" });
            // res.json({ message: "book deleted" });

            res.status(204).end();
        })
    });
}
