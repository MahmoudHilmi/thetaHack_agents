import cloudinary from "../config/cloudinary.js";

export const cloudinaryUploader = (buffer, folder = "uploads", options = {}) => {

  // create a promise to upload
  return new Promise((resolve, reject) => {

    // create a readable stream from the buffer
    const stream = cloudinary.uploader.upload_stream(
      {
        folder: folder,
        resource_type: "auto",
        ...options,
      },
      // handle the result
      (error, result) => {
        if (error) return reject(error);
        resolve(result);
      }
    );

    // 
    stream.end(buffer);
  });
};