import re

image_compile = re.compile(r'[\w]+[a-z]+[\w]+')
version_compile = re.compile(r'[\w.]+\.[\d]+$')


image_and_version_input = """exercisev2:1.7.9.3
aicard:1.4.5.3"""

image_and_version_str = ''
input_list = image_and_version_input.splitlines()
input_len = len(input_list)


# for index, content in enumerate(input_list):
#     image_version_symbol_search = re.search(':', content)
#     print(image_version_symbol_search)
#     # print(image_version_multiple)


if input_len == 1:
    image_and_version_str = image_and_version_input
else:
    # 适配钉钉复制过来的多行格式
    for index, content in enumerate(input_list):
        image_matching = image_compile.fullmatch(content)
        version_matching = version_compile.fullmatch(content)
        image_version_symbol_search = re.search(':', content)
        # 匹配带：的多行
        if image_version_symbol_search:
            image_and_version_str = image_and_version_str + content + ','
        else:
            if image_matching:
                image_name = content
                image_and_version_str = image_and_version_str + image_name + ':'
            elif version_matching:
                image_version = content
                image_and_version_str = image_and_version_str + image_version + ','

print(image_and_version_str.strip(','))
