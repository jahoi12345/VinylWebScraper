from models import VinylStore
from search_engine import search_vinyl_by_artist

vinyl_stores = [
    VinylStore("606 Records", "1808 S Allport St, Chicago, IL 60608", "https://www.606records.com"),
    # Other stores commented out as in original...
]

def main():
    artist_to_search = input("Enter the artist name: ")
    search_vinyl_by_artist(artist_to_search, vinyl_stores)

if __name__ == "__main__":
    main() 