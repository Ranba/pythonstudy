import phonenumbers
from phonenumbers import geocoder, carrier

def get_phone_number_info(phone_number: str):
    try:
        # 提取后 11 位数字
        last_11_digits = phone_number[-11:]
        # 构造标准化的中国手机号码
        formatted_number = "+86" + last_11_digits
        
        # 解析电话号码
        parsed_number = phonenumbers.parse(formatted_number, "CN")
        # 获取归属地信息
        location = geocoder.description_for_number(parsed_number, "zh")  # "zh"表示中文
        # 获取运营商信息
        operator = carrier.name_for_number(parsed_number, "zh")
        
        return {
            "输入号码": phone_number,
            "标准化号码": last_11_digits,
            "归属地": location or "未知",
            "运营商": operator or "未知"
        }
    except phonenumbers.NumberParseException:
        return "无效的电话号码格式！"

if __name__ == "__main__":
    phone_number = input("请输入手机号码：")
    result = get_phone_number_info(phone_number)
    print(result)
