# oxygendemo

##Pre-requisites
- python 2.7
- Scrapy 1.0 ```pip install scrapy```
- PyQuery 1.2.9 ```pip install pyquery```

##My Approach

* The challenge spec indicated that following rules, clean code and the efficiency of my spider were all important aspects to consider in the design of my code. Therefore, my first thoughts were to consider the most efficient way of scraping all unique product items, looking to limit the number of page requests and avoid scraping duplicate items if possible. I spent some time manually navigating the website and inspecting elements to develop assumptions that the 'New In' section of the website did not contain unique items, whilst the 'Sale' category did. I then considered whether to scrape products from individual designer pages or from their sub-category. This would result in a similar number of pages, but as the example item dictionary contains a 'type' field I believed that scraping via categories would be the better approach, as I'd likely be able to identify product types easier this way. 
* From there I noted down each field in the example item and began to explore how best to target this information, making notes on paper at this stage. Some of these early ideas proved valuable, for example I populated the 'code' value with the relevant file name for each product item, and quickly identified the ".brand_name" class for obtaining the name of the designer.
Another early discovery was that sale items differed from regular items, in terms of having two prices (populating different elements of the page), and requiring a sale discount calculation. I initially restricted my spider to scraping just one regular item and one sale item (via only allowing the relevant item urls) so I could work on writing code that would cope with these two different situations. Item price proved quite tricky, for one example.
* I spent a lot of my time in iPython, via ```scrapy shell <url>``` testing my assumptions and understanding the best way to target particular elements. I also made lots of manual notes on paper which was useful to review.
* I implemented one new field at a time before expanding my rules to allow for entire sub-categories, followed by categories and then identified that I could pass the ```ViewAll``` parameter onto the category urls to see all product items under those categories. As I understood this meant I could limit the pages to be scraped down to just four. As the sample data size was fairly small I conducted lots of manual cross-checking, including counting item quantities from the website and comparing them to my crawl results. I also used this approach to confirm that 'New In' items were not unique, as including this url did not increase my item count.
* As I wasn't totally sure whether this was the desired approach in terms of rules and start_urls I also wrote an approach that would target each sub-category url, such as 'Boots' from with the 'Shoes' category. However, this meant that my code for 'type' was no longer consistent, as it was based on the request referrer. So in my initial approach this was always one of those four category pages (with sale items not providing me with any useful information here), whereas the second approach would have required further code to establish which referers belonged to which category, and therefore what type to label the item as. 

##Main Difficulties

* As the tech was new to me I required some time to setup my environment, work through tutorials and solve some problems. A lot of resources are based on using XPath, so I was unsure on exactly how to implement PyQuery for a short while. I used StackOverflow and lots and lots of googling, along with the official Scrapy docs. I also explored the Lyst developer blog, and was able to find some slide decks which provided me with some clues :)
* Images - whilst I had identified how to target just the image urls that I wanted I struggled to find the exact syntax, so this took some time.
* Successfully returning item price from both regular and sale items. The text for these is held within different elements so my code had to identify which element to target and when.
* Stock status - My initial code failed to cope with the wide variations in stock keys used on the website, e.g. "XS", "EU28", "one size", "24" etc. As mentioned below the output of the stock dictionary is not always consistent with how they're listed on the website.
* Item type (jewellery) - as mentioned below. Also, I'd seen the output of 'referer url' in the Scrapy logs so this pointed me in the right direction for help with assigning product types but correctly implementing this was tricky - particularly as the shell offered me no help in this. Initially I returned every referer url from within the item_type method, to help identify/confirm where each item was being refered from.
* In my second approach (with regards to rules) I had a bit of difficulty targeting just the sub-category urls from the left-side navigation (and avoding scraping the designer urls) as both ul's have the same class.

##Improvements

* Labelling jewellery proved tricky and required me manually identifying words which would correctly indicate that an item was one of bracelet, ring, necklace, earring etc. My initial code incorrectly identified the Lark Jumpsuit as jewellery because it's description contained the word 'ring', and highlighted the weakness of using words to set a product's type - however in this instance I couldn't see an alternative solution given the data provided.
* I spent some time exploring the different currency options on the website, to try to provide usd and eur prices (without simply finding the conversion rate and applying this to the gbp price) however was unable to identify exactly how this was being done so opted to focus on the other item fields.
* Similarly, whilst I read the Lyst developer blog articles on item colour and gender these were out of scope for me, particularly as I was limited to standard libraries. I set these to defaults. One thing I could have considered was only setting the gender to female for clothing, shoes and jewellery items as this would have been more accurate. 
* Additionally, the item stock_status dictionaries are not in a consistent order, so this is something that I would look to rectify. 
