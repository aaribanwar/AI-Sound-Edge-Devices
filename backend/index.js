import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";


const port = 8000;
const app = express();
app.listen(port, () => console.log("Listening to the port"));
async function main(){
    await mongoose.connect("mongodb://127.0.0.1:27017/sound");
}

await main()
.then( res => {console.log("MongoDB connection successful")})
.catch( err => { console.log("Connection failed"); console.log(err);});

