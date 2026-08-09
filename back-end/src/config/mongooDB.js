import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();



export const connectDB = async() => {
    try{
        mongoose.set('strictQuery', false)
        await mongoose.connect(process.env.DB_URI)
        console.log("connected to:", mongoose.connection.name)
    }
    catch(error){
        console.log(error.message)
        process.exit(1)
    }
}