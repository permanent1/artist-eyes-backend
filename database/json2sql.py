# -----------------------------------------------------将data.json文件中的数据存储到artist表单中---------------------------------------------
# import json

# # 读取 JSON 文件
# with open('data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # 打开文件以写入 SQL 语句
# with open('artists.sql', 'w', encoding='utf-8') as sql_file:
#     # 生成 SQL 插入语句
#     for artist, info in data.items():
#         sql = f"""INSERT INTO artists (name, year, genre, introduction, background, style, characters, website) VALUES
#         ('{info["name"]}', '{info["year"]}', '{info["genre"]}', '{info["introduction"]}', '{info["background"]}', '{info["style"]}', '{info["Characteristics of the work"]}', '{info["website"]}');\n"""
        
#         # 写入 SQL 语句到文件
#         sql_file.write(sql)

# print("SQL 语句已保存到 artists.sql 文件中。")


# -----------------------------------------------------将data.json文件中的数据存储到artworks表单中---------------------------------------------

# import json

# # 假设 JSON 数据已保存为 artworks.json 文件
# with open('data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # 打开文件以写入 SQL 语句
# with open('artworks.sql', 'w', encoding='utf-8') as sql_file:
#     # 生成 SQL 插入语句
#     for artist, info in data.items():
#         # 插入每个艺术家的三件作品
#         for i in range(1, 4):
#             artwork_key = f'img_{i}'
            
#             sql = f"""INSERT INTO artworks (artist_id, artwork, url) VALUES
#             ('{info["index"]}', '{info[artwork_key]}', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/artist/{info["name"].replace(" ", "%20")}/info/{i}.png');\n"""
            
#             # 写入 SQL 语句到文件
#             sql_file.write(sql)

# print("SQL 语句已保存到 artworks.sql 文件中。")



# -----------------------------------------------------将data.json和data_artwork.json文件中的数据存储到phases表单中---------------------------------------------
# import json

# with open('data.json', 'r', encoding='utf-8') as file:
#     data1 = json.load(file)

# # 打开文件以写入 SQL 语句
# with open('phases1.sql', 'w', encoding='utf-8') as sql_file:
#     # 生成 SQL 插入语句
#     for artist, info in data1.items():
#         # 插入每个艺术家的三件作品
#         i = 1
#         while info.get(f'phase_{i}'):
#             phase_key = f'phase_{i}'
#             phase_name_key = f'phase_{i}_name'
#             phase_introduction_key = f'phase_{i}_introduction'
#             phase_artwork_key = f'phase_{i}_artwork'
#             phase_meaning_key = f'phase_{i}_meaning'

#             # artwork_key = f'phase_{i}_artwork'
#             # background_key = f'art_{i}_background'
#             # style_key = f'art_{i}_style'
#             # theme_key = f'art_{i}_theme'
#             # background_clean = info[background_key].replace('\\', '').replace('"', '').replace("'", '’')

#             sql = f"""INSERT INTO phases (artist_id, phase, name, introduction, artwork, meaning) VALUES
#             ('{info["index"]}','{info[phase_key]}', '{info[phase_name_key].replace("'", '’')}', '{info[phase_introduction_key].replace("'", '’')}', '{info[phase_artwork_key].replace("'", '’')}', '{info[phase_meaning_key]}');\n"""
            
#             # 写入 SQL 语句到文件
#             sql_file.write(sql)

#             i = i + 1

# print("SQL 语句已保存到 phase1.sql 文件中。")

# with open('data_artwork.json', 'r', encoding='utf-8') as file:
#     data2 = json.load(file)

# # 打开文件以写入 SQL 语句
# with open('phases2.sql', 'w', encoding='utf-8') as sql_file:
#     # 生成 SQL 插入语句
#     for artist, info in data2.items():
#         # 插入每个艺术家的三件作品
#         i = 1
#         while info.get(f'phase_{i}_artwork'):

#             artwork_key = f'phase_{i}_artwork'
#             background_key = f'art_{i}_background'
#             style_key = f'art_{i}_style'
#             theme_key = f'art_{i}_theme'

#             background_clean = info[background_key].replace('\\', '').replace('"', '').replace("'", '’')

#             # 构造 SQL UPDATE 语句
#             sql = f"""UPDATE phases
#             SET background = '{background_clean}',
#                 style = '{info[style_key].replace("'", '’')}',
#                 theme = '{info[theme_key].replace("'", '’')}'
#             WHERE artwork = '{info[artwork_key].replace("'", '’')}';\n"""
            
#             # 写入 SQL 语句到文件
#             sql_file.write(sql)

#             i = i + 1

# print("SQL 语句已保存到 phase2.sql 文件中。")
