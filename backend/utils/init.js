const mongoose = require("mongoose");
const User = require("../models/user.js");
const SoundEvent = require("../models/soundEvent.js");
const Notification = require("../models/notification.js");
const CustomSound = require("../models/customSound.js");

async function main(){
    mongoose.connect("mongodb://127.0.0.1:27017/miniProject");
}

await main();
console.log("Conncected to local mongodb");

const userTest = new User({
    name: "sdkvjbdv",
    email: "dklvjndndsvd",
    password: "weifnewn",
    deviceId: "elkn",
    notficationEnabled: false,
    createdAt: Date.now()   
});
await userTest.save();
console.log("inserted a document in user collection");

const soundEventTest = new SoundEvent({
    userId: userTest._id,
    soundType: "Metro",
    confidence: 75
});
await soundEventTest.save();
console.log("sound event document");

const notificationTest = new Notification({
    userId: userTest._id,
    soundEventId: soundEventTest._id,
    method: "alert",
    status: "lol idk"
});
await notificationTest.save();
console.log("notification document working");

const customSoundTest = new CustomSound({
    userId: userTest._id,
    label: "adslicndasc",
    audioSamples: []//dcidnc,
});
await customSoundTest.save();
console.log("dlcfndwcdc");




