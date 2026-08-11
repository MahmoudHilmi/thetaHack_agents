import mongoose from 'mongoose'
import bcrypt from 'bcrypt'

const userSchema = new mongoose.Schema({
    // personal info
    fullName:{type:String, required:true},

    // account info
    email:{type:String, required:true},
    password:{type:String, required:true, select:false},

    // profile image
    avatar: {
        url: { type: String },
        id: { type: String, select: false },
    },
    

    status: {
        type: String,
        enum: ["Active", "Blocked", "Deleted", "Unverified"],
        default: "Unverified"
    },

    // roles
    role:{
        type:String,
        enum: ["Admin", "User"],
        default: "User"
    },

    // verify email 
    verification:{
        code: {type:String},
        expiresAt: {type:Date, default: () => (Date.now() + 10 * 60 * 1000 )},
    },

}, {timestamps:true})

userSchema.methods.checkPassword = async function (password) {
    return await bcrypt.compare(password, this.password)
}

userSchema.index({email:1,createdAt:-1})

const User = mongoose.model('User', userSchema)
export default User



