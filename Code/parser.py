import json
import re
import os


def parse_item(item):
    
    try:
        item_data = {}
        
        item_lines = item.split("\n")
        
        # check item type
        if item_lines[2].strip() == "discontinued product": #or item_lines[3].split(":", 1)[1].strip() != ITEM_TYPE:
            return None
        
        # split groups by 
        id_field = item_lines[0].split(":")[1].strip()
        
        # get each base feature of the group
        item_data["Id"] = id_field
        item_data["ASIN"] = item_lines[1].split(":")[1].strip()
        item_data["title"] = item_lines[2].split(":", 1)[1].strip()
        item_data["group"] = item_lines[3].split(":", 1)[1].strip()
        item_data["salesrank"] = item_lines[4].split(":", 1)[1].strip()
        item_data["similar"] = item_lines[5].split(":")[1].strip().split()
        
        # get each cateogry in item
        categories = [item_lines[6].split(":")[1].strip()]
        index = 7
        
        for _ in range(int(categories[0])):
            categories.append(item_lines[index].strip())
            index += 1
            
        item_data["categories"] = categories
        

        # get review data
        reviews = {}
        rev_line = item_lines[index].split(":", 1)[1].strip().split("  ")
        
        reviews["Id"] = id_field
        reviews["total"] = int(rev_line[0].split(" ", 1)[1])
        reviews["downloaded"] = min(10, int(rev_line[1].split(" ", 1)[1])) 
        reviews["avg rating"] = float(rev_line[2].split(" ", 2)[2])
        
        reviews_data = []
        index += 1
        
        for _ in range(min(10, reviews["downloaded"])):
            # regular expression removes all but one space after cutomer, votes, and/or helpful
            rev = re.sub(r'\b(cutomer|votes|helpful): +', r'\1: ', item_lines[index].strip())
            
            rev = rev.split("  ")
            revi = {
                "date": rev[0].strip(),
                "customer": rev[1].split(" ", 1)[1].strip(),
                "rating": rev[2].split(" ", 1)[1].strip(),
                "votes": rev[3].split(" ", 1)[1].strip(),
                "helpful": rev[4].split(" ", 1)[1].strip()
            }
            
            reviews_data.append(revi)
            index += 1
            
        reviews["reviews"] = reviews_data
        
        return (item_data, reviews)
    
    except Exception as e:
        print(f"error! {str(e)}")
        return None


def run_parser():
    group_data = {}
    all_data = []
    all_reviews = []


    with open("Data/amazon-meta.txt", "r", encoding="utf_8") as file:
        lines = file.read()

    items = lines.split("\n\n")
    
    for item in items:
        result = parse_item(item)

        if result is not None:
            if result[0]["group"] not in group_data:
                group_data[result[0]["group"]] = {
                    "item_data": {},
                    "review_data": {}
                }
            group_data[result[0]["group"]]["item_data"][result[0]["Id"]] = result[0]
            group_data[result[0]["group"]]["review_data"][result[0]["Id"]] = result[1]

            all_data.append(result[0])
            all_reviews.append(result[1])

    for ITEM_TYPE in group_data:
        if not os.path.exists("Data/" + ITEM_TYPE):
            os.mkdir("Data/" + ITEM_TYPE)

        with open("Data/" + ITEM_TYPE + "/" + ITEM_TYPE + ".json", "w") as out:
            json.dump(group_data[ITEM_TYPE]["item_data"], out, indent=2)
            
        with open("Data/" + ITEM_TYPE + "/" + ITEM_TYPE + "_reviews.json", "w") as out:
            json.dump(group_data[ITEM_TYPE]["review_data"], out, indent=2)

    with open("Data/out.json", "w") as out:
        json.dump(all_data, out, indent=2)
    
    with open("Data/out_review.json", "w") as out:
        json.dump(all_reviews, out, indent=2)