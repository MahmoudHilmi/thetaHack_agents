import asyncHandler from 'express-async-handler'
import bcrypt from 'bcrypt'
import jwt from "jsonwebtoken"
import dotenv from 'dotenv'

// utils and config 
import emailTransporter from '../../config/emailTransporter.js'
import { emailVerificationMessage } from '../../utils/emailVerificationMessage.js'
import { cloudinaryUploader } from '../../utils/cloudaniryUploader.js'

// models 
import User from '../../models/user.model.js'
import Session from '../../models/session.model.js'

// 
dotenv.config()


// fields for upload on sign-up route
export const requestedFields = [
    { name: "avatar", maxCount: 1 },
]

export const signUp = asyncHandler(async (req, res) => {
    console.log("EMAIL_USER:", process.env.EMAIL_USER);
    console.log(
      "EMAIL_PASSWORD exists:",
      Boolean(process.env.EMAIL_PASSWORD)
    );

    // check if this email connected with an active account or not
    const account = await User.findOne({ email: req.body.email }).sort({ createdAt: -1 })

    // if there is an account connected with this email
    if (account) {
        // if active
        if (account.status === "Active") {
            return res.status(400).json({ status: "fail", message: "This email is already connected with an active account" })
        }
        // if banned
        else if (account.status === "Blocked") {
            return res.status(400).json({ status: "fail", message: "This email is blocked" })
        }
        // if unverified
        else if (account.status === "Unverified" && account.verification.expiresAt > Date.now()) {
            return res.status(400).json({
                status: "fail",
                action: "verify_email",
                message: "This email is connected with an unverified account, please verify this email or wait for 10 minutes to try again",
            })
        }
    }

    // check required file and upload it
    const avatar = req.files?.avatar ? req.files.avatar[0] : null
    const uploadedAvatar = avatar ? await cloudinaryUploader(avatar.buffer, "avatar") : null

    // hash password, create verification code
    const hashedPassword = await bcrypt.hash(req.body.password, 10)
    const verificationCode = Math.floor(Math.random() * 900000 + 100000).toString()

    // create account
    const newUser = await User.create({
        fullName: req.body.fullName,
        email: req.body.email,
        password: hashedPassword,
        avatar: uploadedAvatar ? { url: uploadedAvatar.url, id: uploadedAvatar.public_id } : null,
        verification: { code: verificationCode },
    })


    // send code to user
    try {
        await emailTransporter.sendMail({
            from: process.env.EMAIL_FROM,
            to: req.body.email,
            subject: "Verify Your Account",
            html: emailVerificationMessage(newUser.fullName, verificationCode)
        })
    } catch (error) {
        console.log(error)
        return res.status(500).json({ status: "fail", message: "Failed to send verification email", error: error.message })
    }

    // create token for verify email
    const token = jwt.sign(
        { _id: newUser._id, email: newUser.email },
        process.env.JWT_SECRET,
        { expiresIn: "10m" }
    )

    // cookie for verify email
    const isProduction = process.env.NODE_ENV === "production";
    res.cookie("Theta-Hack-Auth", token, {
        httpOnly: true,
        secure: isProduction,
        sameSite: isProduction ? "None" : "Lax",
        path: "/",
        maxAge: 10 * 60 * 1000, // 10 minutes
    });

    // create session
    await Session.create({ 
        userId: newUser._id, // reference
        token, // token
        ip: req.ip, // ip address
        agent: req.get("user-agent"), // user agent
        expiresAt: new Date(Date.now() + 10 * 60 * 1000), // 10 minutes
    })

    // response
    res.status(201).json({
        status: "success",
        message: "successful registration, check your email",
        action: "verify_email"
    })
})