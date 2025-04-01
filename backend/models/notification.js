const mongoose = require("mongoose");

async function main(){
    mongoose.connect("mongodb://127.0.0.1:27017/miniProject");
}

await main();

const NotificationSchema = new mongoose.connect({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        default: true
    },
    soundEventId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "SoundEvent",
        required: true
    },
    method: {
        type: String,
        required: true
    },
    status : {
        type: String,
        required: true
    },
    createdAt : {
        type: Date,
        default: Date.now()
    }
});

const Notification = mongoose.model("Notification", NotificationSchema);
module.exports(Notification);
