import phonenumbers
from phonenumbers import geocoder, carrier
import csv


def get_phone_number_info(phone_number: str):
    try:
        # 提取后 11 位数字
        last_11_digits = phone_number.strip()[-11:]
        # 构造标准化的中国手机号码
        formatted_number = "+86" + last_11_digits

        # 解析电话号码
        parsed_number = phonenumbers.parse(formatted_number, "CN")
        # 获取归属地信息
        location = geocoder.description_for_number(parsed_number, "zh")  # "zh"表示中文
        # 获取运营商信息
        operator = carrier.name_for_number(parsed_number, "zh")

        return {
            "原始号码": phone_number,
            "标准化号码": formatted_number,
            "归属地": location or "未知",
            "运营商": operator or "未知"
        }
    except phonenumbers.NumberParseException:
        return {
            "原始号码": phone_number,
            "标准化号码": "无效号码",
            "归属地": "无效",
            "运营商": "无效"
        }


def process_file(input_file: str, output_file: str):
    # 读取输入文件内容
    results = []
    if input_file.endswith('.txt'):
        with open(input_file, 'r', encoding='utf-8') as f:
            phone_numbers = f.readlines()
    elif input_file.endswith('.csv'):
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            phone_numbers = [row[0] for row in reader]  # 假设号码在第一列
    else:
        print("仅支持 .txt 或 .csv 文件！")
        return

    # 处理每个号码
    for phone_number in phone_numbers:
        result = get_phone_number_info(phone_number)
        results.append(result)

    # 将结果写入 CSV 文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["原始号码", "标准化号码", "归属地", "运营商"])
        writer.writeheader()
        writer.writerows(results)

    print(f"处理完成，结果已保存至 {output_file}")


if __name__ == "__main__":
    input_file = input("请输入输入文件路径（.txt 或 .csv）：")
    output_file = input("请输入输出文件路径（.csv）：")
    process_file(input_file, output_file)
