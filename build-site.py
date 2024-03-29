#!/usr/bin/python3

# Build the site

import sys
import os


directory = "."
menu_data = {}
menu_content = ""
page_content = {}
page_settings = {}
index_page_title = ""


if len(sys.argv) > 2:
    sys.stderr.write("Too many arguments!\n")
    sys.exit(1)

if len(sys.argv) == 2:
    directory = sys.argv[1]

if not os.path.isdir(directory):
    sys.stderr.write(directory+" is not a directory!\n")
    sys.exit(1)

for i in ["build", "content"]:
    if not os.path.isdir(i):
        sys.stderr.write(directory+"/"+i+" does not exist!\n")
        sys.exit(1)

output = directory+"/build/"
content = directory+"/content/"

if not len(os.listdir(output)) == 0:
    sys.stderr.write("Build directory is not empty!\n")
    sys.exit(1)


# Read all content files
for c in os.listdir(content):
    title = ""
    category = "0:root"
    desc = ""
    order = 0
    index = False
    hide_menu = False
    in_content = False

    with open(content+c, "r") as cf:
        for line in cf:
            if not in_content:
                if line.startswith("TITLE="):
                    title = line.replace("TITLE=", "").strip()
                    page_content[title] = ""
                    page_settings[title] = []
                elif line.startswith("CATEGORY="):
                    category = line.replace("CATEGORY=", "").strip()
                elif line.startswith("DESC="):
                    desc = line.replace("DESC=", "").strip()
                elif line.startswith("ORDER="):
                    order = int(line.replace("ORDER=", "").strip())
                elif line.startswith("INDEX"):
                    index = True
                elif line.startswith("NOMENU"):
                    hide_menu = True
                elif line.startswith("=="):
                    in_content = True
            else:
                page_content[title] += line

    if hide_menu is True:
        page_settings[title].append("nomenu")

    if category != "" and category not in menu_data.keys():
        menu_data[category] = {}

    if order != 0:
        while order in menu_data[category].keys():
            order += 1

        if index is True:
            index_page_title = title

        menu_data[category][order] = {"TITLE" : title, "DESC" : desc}
    
#print(menu_data)
#print(page_content)

# Build side menu
print("Building side menu.")
for m in sorted(menu_data.keys()):
    category_name = m.split(":")[1]

    if category_name != "root":
        menu_content += "        <p><strong>"+m.split(":")[1]+"</strong></p>\n"

    menu_content += "        <ul>\n"
    for i in sorted(menu_data[m].keys()):
        if menu_data[m][i]["TITLE"] != "":
            if index_page_title == menu_data[m][i]["TITLE"]:
                filename = "index"
            else:
                filename = menu_data[m][i]["TITLE"].replace(" ", "_")
            menu_content += "          <li><a href='"+filename+".html'>"+menu_data[m][i]["TITLE"]+"</a></li>\n"
        if menu_data[m][i]["DESC"] != "":
            menu_content += "          <span class='link-subtext'>"+menu_data[m][i]["DESC"]+"</span>\n"
    menu_content += "        </ul>\n"

#print(menu_content)

# Generate pages
print("Generating pages.")
for p in page_content.keys():
    if index_page_title == p:
        filename = output+"index.html"
    else:
        filename = output+p.replace(" ", "_")+".html"
    print("Creating "+filename)
    with open(filename, "w") as outfile:
        outfile.write("<!doctype html>\n")
        outfile.write("  <head>\n")
        outfile.write("    <link rel='stylesheet' href='css/style.css'>\n")
        outfile.write("    <title>NATHAN242's Projects</title>\n")
        outfile.write("  </head>\n")
        outfile.write("  <body>\n")
        outfile.write("    <div class='top-section'>\n")
        outfile.write("      <p>NATHAN242's Projects</p>\n")
        outfile.write("    </div>\n")

        if "nomenu" in page_settings[p]:
            outfile.write(page_content[p])
        else:
            outfile.write("    <div class='cols'>\n")
            outfile.write("      <div class='left-section'>\n")

            outfile.write(menu_content)

            outfile.write("      </div>\n")

            outfile.write("      <div class='right-section'>\n")
            outfile.write("        <br>\n")

            outfile.write(page_content[p])
        
            outfile.write("      </div>\n")
            outfile.write("    </div>\n")

        outfile.write("  </body>\n")
        outfile.write("</html>")
        
