import asyncHandler from 'express-async-handler'
import jwt from "jsonwebtoken"
import User from '../../models/user.model.js'
import Session from '../../models/session.model.js'
import dotenv from 'dotenv'

dotenv.config()

export const verifyEmail = asyncHandler(async (req, res) => {
    const { code } = req.body
    
    // Try to get email from req.user
    const email = req.user?.email || req.body.email

    // check code from body
    if (!code) {
        return res.status(400).json({ status: "fail", message: "Verification code is required" })
    }

    // check if user in database
    const user = await User.findOne({ email }).sort({ createdAt: -1 })
    if (!user) {
        return res.status(404).json({ status: "fail", message: "Account not found. Please check your email or create a new account." })
    }

    // check if user is already verified
    if (user.status !== "Unverified") {
        return res.status(400).json({ status: "fail", message: `This email is already ${user.status}.` })
    }

    // check if code is correct
    if (user.verification.code !== code) {
        return res.status(400).json({ status: "fail", message: "Incorrect verification code." })
    }

    // Generate new token
    const token = jwt.sign(
        { _id: user._id, email: user.email, role: user.role }, 
        process.env.JWT_SECRET, 
        { expiresIn: "30d" }
    )

    // clear the temporary cookie if it exists
    res.clearCookie("Theta-Hack-Auth")


    // recover old session if exists
    const oldSession = await Session.findOne({ userId: user._id }).sort({ createdAt: -1 })
    if (oldSession) {
        oldSession.status = "revoked"
        oldSession.revokedReason = "Account verified"
        await oldSession.save()
    }

    // create new session
    await Session.create({
        userId: user._id,
        token: token,
        ip: req.ip,
        agent: req.get("user-agent"),
        expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
    })

    // update DB
    user.status = "Active"
    // user.verification.verificationCode = null;
    // user.verification.expiresAt = null;
    user.set("verification", undefined);
    await user.save()    

    // set new production cookie
    const isProduction = process.env.NODE_ENV === "production";
    res.cookie("Theta-Hack-Auth", token, {
        httpOnly: true,
        secure: isProduction,
        sameSite: isProduction ? "None" : "Lax",
        path: "/",
        maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
    })

    // response
    return res.status(200).json({
        status: "success",
        message: "Email verified successfully",
        data: {
            _id: user._id,
            email: user.email,
            role: user.role,
            status: user.status
        }
    });
})

export default verifyEmail