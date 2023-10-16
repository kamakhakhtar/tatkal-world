import requests
import hashlib

base_url = "http://3.111.109.85:8088/ch/getPh"

ch_name = "Lak5a8x"
time = "180"
secret_key = "73ryf"

# Calculate the MD5 hash of the signature string
signature_string = f"{ch_name}{time}{secret_key}"
signature = hashlib.md5(signature_string.encode()).hexdigest()

print(f"ChName : {ch_name}")
print(f"time : {time}")
print(f"Secret Key : {secret_key}")
print(f"Signature String : {signature_string}")
print(f"Signature Hash : {signature}")

# Construct the parameters for the request
params = {
    "chName": ch_name,
    "time": time,
    "sign": signature  # Remove "SignatureString:" from the signature value
}

# Make the HTTP GET request
response = requests.get(base_url, params=params)

# Print the response content
print(response.text)
