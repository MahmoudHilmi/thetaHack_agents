import express from 'express'
import upload from '../middlewares/upload.middleware.js'
import { signUp, requestedFields } from '../controllers/auth/sign-up.js'
import { Sign_in } from '../controllers/auth/log-in.js'
import { verifyToken } from '../middlewares/verifyToken.middleware.js'
import { verifyEmail } from '../controllers/auth/verify-email.js'
import { logout } from '../controllers/auth/log-out.js'
import VerifyMe from '../controllers/auth/verifyMe.js'


const authRouter = express.Router()

// sign up
authRouter.post('/sign-up', upload.fields(requestedFields), signUp)

// sign in
authRouter.post('/sign-in', Sign_in)

// verify email
authRouter.post('/verify-email', verifyToken("Theta-Hack-Auth"), verifyEmail)

// verify me
authRouter.get('/verify-me', verifyToken("Theta-Hack-Auth"), VerifyMe)

// log out
authRouter.post('/log-out', verifyToken("Theta-Hack-Auth"), logout)

// check if auth
authRouter.get('/check-auth', verifyToken("Theta-Hack-Auth"), VerifyMe)


export default authRouter