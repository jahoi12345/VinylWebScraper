import sys
from functools import partial

print = partial(print, flush=True, file=sys.stdout)

from models import VinylStore

def search_vinyl_by_artist(artist, vinyl_stores):
    if not artist.strip():
        print("❌ Please enter a valid artist name.")
        return

    found_stores = []
    total_stores = len(vinyl_stores)
    
    print(f"\n🔍 Searching for '{artist}' in {total_stores} Chicago record stores...\n")
    
    for i, store in enumerate(vinyl_stores, 1):
        print(f"Checking store {i}/{total_stores}: {store.name}")
        try:
            if store.search_artist(artist):
                found_stores.append(store)
        except Exception as e:
            print(f"⚠️ Error searching {store.name}: {str(e)}")

    if found_stores:
        print(f"\n✅ Vinyls by {artist} are available at {len(found_stores)} store(s):")
        for store in found_stores:
            print(f"- {store.name} ({', '.join(store.locations)})")
            print(f"  Websites: {', '.join(store.websites)}\n")
    else:
        print(f"\n❌ No records found for {artist} in the {total_stores} indexed stores.")
