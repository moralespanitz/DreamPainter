import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Log the configuration
# ==============================

config = cloudinary.config( 
  cloud_name = "dmzkmu2fo", 
  api_key = "385427175728496", 
  api_secret = "s6BcrxAKm5my1rKI8-GD0kDfZ8c" 
)

def uploadImage():
    imgs_origin_folder = "imgs"
    img_file_name = "tree2.jpeg"
    target_folder = "open-day-cs"
    img_code = "img_0004"

    cloudinary.uploader.upload("woman.jpg", public_id=img_code, unique_filename = False, overwrite=True)
    # Build the URL for the image and save it in the variable 'srcURL'
    srcURL = cloudinary.CloudinaryImage(img_code).build_url()
    # Log the image URL to the console. 
    # Copy this URL in a browser tab to generate the image on the fly.
    print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")

if __name__ == "__main__":
    uploadImage()