var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var OmokSchema = new Schema({
    id: String,
    xy: Number
});

module.exports = mongoose.model('Omok', OmokSchema);
