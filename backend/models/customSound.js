const mongoose = require("mongoose");

async function main(){
    mongoose.connect("mogngodb://127.0.0.1:27017/miniProject");
}

await main();

const CustomSoundSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    label: {
        type: String,
        required: true
    }, //array below of file paths for training
    audioSamples: [{
        type: String,
        required: true
    }] ,
    createdAt: {
        type: Date,
        default: Date.now()
    }
});

const CustomSound = mongoose.model("CustomSound",CustomSoundSchema);

module.exports(CustomSound);