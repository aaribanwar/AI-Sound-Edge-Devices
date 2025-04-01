const mongoose = require("mongoose");

async function main(){
    mongoose.connect("mongodb://127.0.0.1:27017/miniProject");
}

await main();

const UserSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    deviceId: {
        type: String
    },
    notificationEnabled: {
        type: Boolean,
        default: true
    },
    createdAt: {
        type: Date,
        default: Date.now()
    }
});

const User = mongoose.model("User",UserSchema);

module.exports(User);