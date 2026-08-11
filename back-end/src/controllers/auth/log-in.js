import asyncHandler from 'express-async-handler'
import bcrypt from 'bcrypt'
import jwt from "jsonwebtoken"
import User from '../../models/user.model.js'
import Session from '../../models/session.model.js'
import dotenv from 'dotenv'

dotenv.config()

export const Sign_in = asyncHandler(async (req, res) => {
    const { email, password } = req.body

    // 1. check if email and password are provided
    if (!email || !password) {
        return res.status(400).json({ status: "fail", message: "Please provide email and password" })
    }

    // 2. find user by email
    const user = await User
        .findOne({ email }).sort({ createdAt: -1 }).select("+password")

    // 3. check if user exists
    if (!user) {
        return res.status(401).json({ status: "fail", message: "This email doesn't belong to any account" })
    }
    const isPasswordMatch = await bcrypt.compare(password, user.password)

    // 4. check user status
    if (["Blocked", "Deleted"].includes(user.status)) {
        return res.status(403).json({ status: "fail", message: `This account has been ${user.status}.` })
    }
    else if (user.status === "Unverified" 
            && isPasswordMatch 
            && user.verification.expiresAt > Date.now()) {
        return res.status(401).json({
            status: "fail",
            action: "verify_email",
            message: "This account is not verified. Please verify your email first."
        })
    }
    else if (user.status === "Unverified" && user.verification.expiresAt < Date.now()){
        return res.status(401).json({
            status: "fail",
            message: "This account is not exist, please sign up again" 
        })
    }


    // 5. compare password
    if (!isPasswordMatch) {
        return res.status(401).json({ status: "fail", message: "password is incorrect" })
    }

    // 6. generate JWT token
    const token = jwt.sign(
        { _id: user._id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: "30d" }
    )

    // 7. create session
    await Session.create({
        userId: user._id,
        token: token,
        ip: req.ip,
        agent: req.get("user-agent"),
        expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
    })

    // 8. set cookie
    const isProduction = process.env.NODE_ENV === "production"
    res.cookie("Theta-Hack-Auth", token, {
        httpOnly: true,
        secure: isProduction,
        sameSite: isProduction ? "None" : "Lax",
        path: "/",
        maxAge: 30 * 24 * 60 * 60 * 1000 // 30 days
    })

    // 9. return response
    res.status(200).json({
        status: "success",
        message: "Logged in successfully",
        data: {
            _id: user._id,
            email: user.email,
            role: user.role,
        }
    })
})