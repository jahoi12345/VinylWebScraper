from models import VinylStore
from search_engine import search_vinyl_by_artist

vinyl_stores = [
    VinylStore("Reckless Records", ["1379 N Milwaukee Ave, Chicago, IL 60622", "929 W Belmont Ave, Chicago, IL 60657", "26 E Madison St, Chicago, IL 60602"], "https://www.reckless.com"),
    VinylStore("Pinwheel Records", "1722 W 18th St, Chicago, IL 60608", ["https://www.pinwheelrecords.com", "https://www.discogs.com/seller/pinwheelrecordschi/profile", "https://www.ebay.com/str/pinwheelrecords"]),
    VinylStore("Groove Distribution", "346 N Justine St, Chicago, IL 60607", ["https://www.groovedis.com", "https://www.groovedis.com/shop/Stock-p-1-c-263.html"]),
    VinylStore("Loud Pizza Records", "2833 W Fullerton Ave, Chicago, IL 60647", "https://loudpizza.com/"),
    VinylStore("Rattleback Records", "5405 N Clark St, Chicago, IL 60640", "https://store.rattlebackrecords.com/"),
    VinylStore("Meteor Gem", "3542 S Halsted St, Chicago, IL 60609", "https://meteor-gem.com/?"),
    VinylStore("Let's Boogie Records and Tapes", "3321 S Halsted St, Chicago, IL 60608", ["https://www.letsboogierecords.com", "https://www.discogs.com/seller/lets_boogie_records/profile"]),
    VinylStore("Shady Rest Vintage and Vinyl", "1659 W 18th St, Chicago, IL 60608", "https://www.shadyrestchicago.com/"),
    VinylStore("Thrill Jockey Records", "2044 W Chicago Ave, Chicago, IL 60622", "https://www.thrilljockey.com"),
    VinylStore("Out of the Past Records", "4407 W Madison St, Chicago, IL 60624", ["https://www.outofthepastrecords.com", "https://outofthepastrecords.myshopify.com/"]),
    VinylStore("Dusty Groove", "1120 N Ashland Ave, Chicago, IL 60622", "https://www.dustygroove.com"),
    VinylStore("606 Records", "1808 S Allport St, Chicago, IL 60608", "https://www.606records.com"),
    VinylStore("Bric-A-Brac Records and Collectibles", "2845 N Milwaukee Ave, Chicago, IL 60618", ["https://www.bricabracrecords.com", "https://www.discogs.com/seller/bricabracrecords/profile"]),
    VinylStore("Gramaphone Records", "2843 N Clark St, Chicago, IL 60657", "https://www.gramaphonerecords.com"),
    VinylStore("Record Breakers", "2935 N Milwaukee Ave, Chicago, IL 60618", ["https://www.recordbreakerschi.com", "https://shop.recordbreakerschi.com/"]),
    VinylStore("Round Trip Records", "3455 W Foster Ave, Chicago, IL 60625", ["https://roundtriprecords.store/?", "https://www.discogs.com/seller/RoundTripRecords/profile"]),
    VinylStore("Tone Deaf Records", "4356 N Milwaukee Ave, Chicago, IL 60641", "https://www.tonedeafrecs.com"),
    VinylStore("Music Direct", "1811 W Bryn Mawr Ave, Chicago, IL 60660", "https://www.musicdirect.com"),
    VinylStore("Miyagi Records", "307 E Garfield Blvd, Chicago, IL 60637", "https://www.miyagirecords.com"),
    VinylStore("Bob's Blues & Jazz Mart", "3419 W Irving Park Rd, Chicago, IL 60618", ["https://www.discogs.com/user/bluesandjazzmart/collection", "https://www.ebay.com/str/bluesandjazzmart"]),
    VinylStore("Vintage Vinyl", "925 Davis St, Evanston, IL 60201", "https://www.vintagevinyl.com"),
    VinylStore("Shuga Records", "1272 N Milwaukee Ave, Chicago, IL 60622", "https://www.shugarecords.com"),
]

def main():
    artist_to_search = input("Enter the artist name: ")
    search_vinyl_by_artist(artist_to_search, vinyl_stores)

if __name__ == "__main__":
    main() 
