import jwt from 'jsonwebtoken'
import dotenv from 'dotenv'
import asyncHandler from 'express-async-handler'

// models
// import Sessions from "../models/session.model.js"

dotenv.config()

export const verifyToken = (cookieName, ...allowedRoles) => asyncHandler(async(req, res, next) => {
    // get token
    const token = req.cookies[cookieName]
    if(!token) {
        return res.status(401).json({status:"fail", message: "No token provided" })
    }

    // verify token
    let decodedToken
    try {
        decodedToken = jwt.verify(token, process.env.JWT_SECRET)
    } catch (error) {
        return res.status(401).json({status:"fail", message: "Invalid or expired token" })
    }

    // check if user has allowed role
    if(allowedRoles.length > 0 && !allowedRoles.includes(decodedToken.role)) {
        return res.status(403).json({status:"fail", message: "You don't have permission to access this resource" })
    }

    // check if token exist in DB
    // const userSession = await Sessions.findOne({token: token})

    // check if token is valid
    // if(!userSession) {
    //     return res.status(401).json({status:"fail", message: "Invalid token" })
    // }

    // // check if session is revoked
    // if(userSession.status === "revoked") {
    //     return res.status(401).json({status:"fail", message: "Your session has been revoked" })
    // }
    
    // attach user to request
    req.user = decodedToken
    next()
})