import User from "../../models/user.model.js"
import asyncHandler from 'express-async-handler';

// verify-me 
const VerifyMe = asyncHandler(async (req, res) => {
    // check if user in dataBase or not
    if (!req.user?._id) {
        return res.status(401).json({ status: "fail", message: "Unauthorized", data: null });
    }

    // get user from dataBase
    const user = await User.findById(req.user._id)

    // check if user not found
    if (!user) {
        return res.status(404).json({ status: "fail", message: "User not found", data: null });
    }

    // check if user is active or unverified
    const userStatus = user.status
    if (userStatus !== "Active" && userStatus !== "Unverified") {
        return res.status(401).json({ status: "fail", message: "Unauthorized", data: null });
    }

    // response
    return res.status(200).json({
        status: "success",
        message: "User verified successfully",
        data: {
            user: {
                _id: user._id,
                role: user.role,
                status: user.status,
                email: user.email,
                fullName: user.fullName,
                avatar: user.avatar?.url || null,
            }
        }
    });
})

export default VerifyMe