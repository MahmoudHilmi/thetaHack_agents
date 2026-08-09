import {validationResult } from "express-validator"


// check data using schema
export const validator = (checkSchema) => {
    // get all validators
    const validatorArrays = Object.values(checkSchema)
    
    // run validators
    return async (req,res,next) => {

        // run all validators
        await Promise.all(validatorArrays.map(v => v.run(req)))

        // get errors
        const errors = validationResult(req).array({onlyFirstError:true}) || []

        // if errors
        if(errors.length) {
            let errorsOBJ = {}
            errors.forEach( error => errorsOBJ[error.path] = error.msg)
            return res.status(400).json({status:"validation", message:"Validation failed", data: {errors: errorsOBJ}})
        }
        
        // next middleware
        next()
    } 
}