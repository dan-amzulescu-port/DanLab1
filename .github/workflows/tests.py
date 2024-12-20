

import json

str = '\"{\\"inputs\\":{\\"requires_s_3\\":false,\\"requires_ec_2\\":false,\\"ttl\\":\\"1 Day\\",\\"project\\":{\\"identifier\\":\\"apollo\\",\\"title\\":\\"Apollo\\",\\"icon\\":\\"Travel\\",\\"blueprint\\":\\"projects\\",\\"team\\":[\\"Gandalf\\",\\"Sith\\",\\"Frodo\\"],\\"properties\\":{\\"name\\":null},\\"relations\\":{},\\"createdAt\\":\\"2024-12-11T23:01:08.935Z\\",\\"createdBy\\":\\"user_sS0z4qLF1d61RC7v\\",\\"updatedAt\\":\\"2024-12-11T23:01:08.935Z\\",\\"updatedBy\\":\\"user_sS0z4qLF1d61RC7v\\"},\\"project_id\\":\\"apollo\\"},\\"runId\\":\\"r_hsjzluqCu2FafYCI\\",\\"triggered_by\\":\\"dan.amzulescu+lab1@gmail.com\\"}\"'
str = '\"{\\"inputs\\":{\\"requires_s_3\\":false,\\"requires_ec_2\\":false,\\"ttl\\":\\"1 Day\\",\\"project\\":{\\"identifier\\":\\"apollo\\",\\"title\\":\\"Apollo\\",\\"icon\\":\\"Travel\\",\\"blueprint\\":\\"projects\\",\\"team\\":[\\"Gandalf\\",\\"Sith\\",\\"Frodo\\"],\\"properties\\":{\\"name\\":null},\\"relations\\":{},\\"createdAt\\":\\"2024-12-11T23:01:08.935Z\\",\\"createdBy\\":\\"user_sS0z4qLF1d61RC7v\\",\\"updatedAt\\":\\"2024-12-11T23:01:08.935Z\\",\\"updatedBy\\":\\"user_sS0z4qLF1d61RC7v\\"},\\"project_id\\":\\"apollo\\"},\\"runId\\":\\"r_hsjzluqCu2FafYCI\\",\\"triggered_by\\":\\"dan.amzulescu+lab1@gmail.com\\"}\"'

str2 = str.replace("\\", '')
str3 = str2.replace('"{', '{')
str4 = str3.replace('}"', '}')
json_str = json.loads(str4)
print()