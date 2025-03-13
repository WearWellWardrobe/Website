
import django
import os
import random
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE','projectSite.settings')
django.setup()
from WearWellWardrobe.models import Category, Page


def populate():
    categories = {
        "Access":{'name':'Access'},         # 1
        "Storage":{'name':'Storage'},       # 2
        "Maintain":{'name':'Maintain'},     # 3
        "Adaptation":{'name':"Adaptation"}, # 4    
        "Disposal":{'name':'Disposal'},     # 5

        "Landfill":{'name':'Landfill'},     # 6
    }
    
    for k,v in categories.items():
        cat = Category.objects.get_or_create(
            name=v['name'],
            
        )
    
    pages = {
    # in form: cat. ID, title, c1, c2, c3, c4, im1, displayStyle , pageNotes, deletable (True)
        1:[1, "Access", "Before purchasing, consider the following;\n Do you love it before you buy it?\n How often will you wear it? \nCan you afford it?\n What is the fabric composition? \nCan I wash it?", "When deciding to purchase a garment, you can check the sustainability rating of a brand using GoodOnYou.", "https://directory.goodonyou.eco/ ", "", None, 1,  "A page made by the population script", True],
        2:[1, "Lease", "Clothing can be leased via rental platforms and local rental facilities. Experts Eco-Age states you should get 30 wears out of every garment, renting out your clothes makes this possible. ", "https://www.fairwear.org/join-the-movement/how-to-wear-fair/ ", "https://www.hurrcollective.com/https://byrotation.com/?srsltid=AfmBOoqcoBDI0dpqvz3J2by_oGRGwr8ujcc1iDbTNQzpmEo-LnzaCtHu", "", None, 1,  "A page made by the population script", True],
        3:[1, "Rent", "Renting out mid-high-end fashion garments has never been easier, for a fraction of the price you can rent clothing locally and online.", "https://www.vogue.co.uk/article/clothing-rental-siteshttps://www.stylist.co.uk/fashion/dress-hire-where-to-rent-designer-clothes-sustainable-fashion/325981 ", "", "", None, 1,  "A page made by the population script", True],
        4:[1, "Share in and Out", "Clothes swapping events can lead to the exchange of pre-loved clothing, freshening up wardrobes in a fun social setting.", "Glasgow University Eco Hub has a swap service available for students and visitors to swap their clothes with the items donated.https://www.facebook.com/profile.php?id=100088956199816# ", "", "", None, 1,  "A page made by the population script", True],
        5:[3, "Maintain", "It’s important to know how to maintain garments already owned, making them last longer.", "https://mylittlegreenwardrobe.com/blogs/news/love-your-clothes-10-eco-friendly-ways-to-care-for-your-clothes?srsltid=AfmBOoohaRJYygiY8AKbNoQZKg09izNsIGvy-th150o79cdW8sn7V8yo", "", "", None, 1,  "A page made by the population script", True],
        6:[3, "Wash Less", "Always read the garment care label. It’s best to wash clothes less and at low temperatures (30*) for the best impact possible on the environment.", "See the Image for the table of wears", "●	Lightly soiled clothing can be spot-cleaned, and dirt can be cleaned off coats and jackets using a clothes brush. \n●	Airing clothing outside can eliminate bad odours as the UV rays can kill bacteria, \n●	Spraying garments with a fabric spray can keep garments smelling fresh for longer\n●	Using an old pillowcase to put delicates (underwear) in when washing.\n", "https://www.armandhammer.com/articles/fabric-guide-for-how-to-wash-different-fabrics ", None, 1,  "A page made by the population script", True],
        7:[3, "Repair", "Mending garments is an easy and inexpensive way to extend a garment's life cycle. Small sewing tasks can be learnt in the home or taken to a tailor or garment repair shop.", "Repair What You Wear is an educational resource for anyone interested in repairing and mending clothing through tutorials and written guides on basic sewing techniques.", "https://repairwhatyouwear.com/ ", "In the UK, continuing to wear a garment for 9 months longer, could diminish its environmental impacts by 20-30%. ", None, 1,  "A page made by the population script", True],
        8:[2, "Storage", "When storing garments, they must be stored correctly to be kept in the best possible condition.", "https://www.asket.com/gb/lifecycle/care/storage ", "", "", None, 1,  "A page made by the population script", True],
        9:[2, "Clear Out ", "Where is best to dispose of garments? Is this garment resellable? Past the point of repair? ", "Bobbling, pilling, stains and smells are all factors that influence the clearing out of clothing. Before throwing out, consider these alternatives;\n●	A pilling comb or lint remover can help to remove bobbles or fuzz. \n●	Clothing odours and stains can be removed with everyday household products; baking soda, lemon juice and vinegar.", "", "", None, 1,  "A page made by the population script", True],
        10:[2, "Pest Control", "Moths are carnivorous creatures that fester in dark, undisturbed places like wardrobes and closets, eating into our knitwear and jersey causing little to large holes in fabric. ", "https://www.totalwardrobecare.co.uk/pages/5-steps-to-a-moth-free-wardrobe?srsltid=AfmBOoqm3Ht8MFqLTBfJK80UiOm_lVvvwmEkPeRpijTaPSsAGt7Y4PnA ", "Here are some solutions to deterring moths;\n●	Make sure to inspect second-hand clothing for moth holes before purchasing.\n●	Freezing garments in a sealed plastic bag at -18* for 2 weeks will kill all moths. Once removed from the freezer, vacuum them to remove all debris.\n●	Do a spring clean, moths are most active between spring to summer.", "", None, 1,  "A page made by the population script", True],
        11:[4, "Adapt", "Bobbling and pilling can occur in loose knitted fabrics, and less so in densely knitted or woven fabrics.", "https://www.jmldirect.com/bobble-off-v3-bobble-and-lint-remover-keeps-fabrics-looking-brand-new?srsltid=AfmBOopv7j9DO308CfNvI-_4eLKTcA-Ba0CD8rlR1wlj3ZNayhEe9I_Chttps://www.oxfam.org.uk/oxfam-in-action/oxfam-blog/how-to-darn/ ", "", "", None, 1,  "A page made by the population script", True],
        12:[4, "Downcycle", "Downcycling converts discarded clothing into an item of lower value, like turning a t-shirt into old cleaning rags.", "https://slate.com/life/2024/11/donate-clothes-landfill-solution-rags-recylce.html ", "", "", None, 1,  "A page made by the population script", True],
        13:[4, "Upcycle", "Upcycling converts discarded clothing into a new useable form, increasing the product's value", "https://fashionjournal.com.au/fashion/designers-old-clothes/ ", "", "", None, 1,  "A page made by the population script", True],
        14:[5, "Responsible Disposal", "All clothing and shoes can be taken to the clothing recycling bank. Put all clothing in a clean plastic bag before putting it into the clothing bank.", "https://glasgowgis.maps.arcgis.com/apps/webappviewer/index.html?id=345f389a91ff4f1fa193b24df832fb05https://glasgowgis.maps.arcgis.com/apps/webappviewer/index.html?id=345f389a91ff4f1fa193b24df832fb05 ", "", "", None, 1,  "A page made by the population script", True],
        15:[5, "Sell", "You can sell your garments via second-hand access points, in person or online.", "https://www.vinted.co.uk/ https://www.depop.com/gb/", "", "", None, 1,  "A page made by the population script", True],
        16:[5, "Pass It On", "When donating to charity, think, would you wear it? ", "https://www.clothingcollective.org/post/the-do-s-and-don-ts-of-clothing-donations#:~:text=Clothes%20which%20are%20a%20little,have%20gone%20to%20better%20use. ", "", "", None, 1,  "A page made by the population script", True],       
        17:[6, "Landfill", "Incineration is the process of burning clothing to dispose of unwanted materials.Landfill is the disposal of unwanted clothing, buried on a waste area of land. ", "73% of all textiles end up in landfill or incineration.https://www.letsrecycle.com/news/incineration-of-textiles-could-cost-uk-economy-200m/", "", "", None, 1,  "A page made by the population script", True],
        18:[1, "Charity Shops", "A sustainable place to shop for new clothes is charity shops.", "Many items of clothing don't need to be purchased brand new. Buying from charity shops reduces the number of new clothing needed and is often much cheaper than buying brand new!", "", "", None, 1,  "A page made by the population script", True],    
        19:[1, "Online shopping", "Where possible, shop second-hand for clothes online on sites like Vinted or Depop instead of buying brand new clothes from fast fashion brands. ", "https://www.depop.com/gb/", "https://www.vinted.co.uk", "", None, 1,  "A page made by the population script", True],    
        20:[1, "Sustainable shopping", "If you must buy a clothing item brand new, it is important to know which materials are the most sustainable. ", "Check out the Good on You Sustainability Checker app to find this out.", "", "", None, 1,  "A page made by the population script", True],    

    }
    
    for pageID, contents in pages.items():
        category, created = Category.objects.get_or_create(ID=contents[0])
        
        page = Page.objects.create(
            category=category,
            title=contents[1],
            content1=contents[2],
            content2=contents[3],
            content3=contents[4],
            content4=contents[5],
            img1=contents[6],
            displayStyle =contents[7],

            pageNotes=contents[8],
            deletable=contents[9]
        )
        print(f"Added page: {page.title} under category: {category.name}")



if __name__ == '__main__':
    print("Starting Population Script for WearWellWardrobe")
    populate()