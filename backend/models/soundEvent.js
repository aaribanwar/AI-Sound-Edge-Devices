const mongoose = require("mongoose");

async function main(){
    mongoose.connect("mongodb://127.0.0.1:27017/miniProject");
}

await main();

const soundSchema = new mongoose.Schema({
    userId : {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        required: true 
    },
    soundType: {
        type: String,
        required: true
    },
    confidence: {
        type: Number,
        required: true
    },
    timestamp: {
        type: Date,
        default: Date.now
    },
    alerted: {
        type: Boolean, default: false
    }
});

const SoundEvent = mongoose.model("SoundEvent",soundSchema);
module.exports(SoundEvent); 